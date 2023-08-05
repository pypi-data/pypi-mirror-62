"""SWF decisions making."""

import json
import typing as t
import logging as lg

from . import _base

logger = lg.getLogger(__name__)
_at_attr_keys = {
    "ActivityTaskCompleted": "activityTaskCompletedEventAttributes",
    "ActivityTaskFailed": "activityTaskFailedEventAttributes",
    "ActivityTaskTimedOut": "activityTaskTimedOutEventAttributes",
    "ActivityTaskScheduled": "activityTaskScheduledEventAttributes",
    "ActivityTaskStarted": "activityTaskStartedEventAttributes",
}


def _get(item_id, items, id_key):
    """Get item from list with given ID."""
    return next(item for item in items if item[id_key] == item_id)


class DAGBuilder(_base.DecisionsBuilder):
    """SWF decision builder from DAG-type workflow specification."""

    def __init__(self, workflow: "DAGWorkflow", task):
        super().__init__(workflow, task)
        self._scheduled = {}
        self._activity_task_events = {at["id"]: [] for at in workflow.task_specs}

    def _schedule_task(
        self,
        activity_task: t.Dict[str, t.Any],
        workflow_started_event: t.Dict[str, t.Any],
    ):
        assert workflow_started_event["eventType"] == "WorkflowExecutionStarted"
        attrs = workflow_started_event["workflowExecutionStartedEventAttributes"]
        decision_attributes = {
            "activityId": activity_task["id"],
            "activityType": activity_task["type"],
        }

        input_ = json.loads(attrs.get("input", "null"))
        if input_:
            decision_attributes["input"] = json.dumps(input_[activity_task["id"]])
        if "heartbeat" in activity_task:
            decision_attributes["heartbeatTimeout"] = str(activity_task["heartbeat"])
        if "timeout" in activity_task:
            decision_attributes["startToCloseTimeout"] = str(activity_task["timeout"])
        if "task_list" in activity_task:
            decision_attributes["taskList"] = {"name": activity_task["task_list"]}
        if "priority" in activity_task:
            decision_attributes["taskPriority"] = str(activity_task["priority"])

        decision = {
            "decisionType": "ScheduleActivityTask",
            "scheduleActivityTaskDecisionAttributes": decision_attributes,
        }
        self.decisions.append(decision)

    def _get_scheduled_references(self):
        for event in self.task["events"]:
            if event["eventType"] in _at_attr_keys:
                if event["eventType"] == "ActivityTaskScheduled":
                    self._scheduled[event["eventId"]] = event
                else:
                    attrs = event[_at_attr_keys[event["eventType"]]]
                    self._scheduled[event["eventId"]] = _get(
                        attrs["scheduledEventId"], self.task["events"], "eventId"
                    )

    def _get_activity_task_events(self):
        for event in self.task["events"]:
            if event["eventType"] in _at_attr_keys:
                scheduled_event = self._scheduled[event["eventId"]]
                attrs = scheduled_event["activityTaskScheduledEventAttributes"]
                self._activity_task_events[attrs["activityId"]].append(event)

    def _process_activity_task_completed_event(self, event: t.Dict[str, t.Any]):
        # Schedule dependants
        scheduled_event = self._scheduled[event["eventId"]]
        attrs = scheduled_event["activityTaskScheduledEventAttributes"]
        dependants_task = self.workflow.dependants[attrs["activityId"]]

        for activity_task_id in dependants_task:
            assert not self._activity_task_events[activity_task_id]
            activity_task = _get(activity_task_id, self.workflow.task_specs, "id")

            dependencies_satisfied = True
            for dependency_activity_task_id in activity_task["dependencies"]:
                events = self._activity_task_events[dependency_activity_task_id]
                if not events or events[-1]["eventType"] != "ActivityTaskCompleted":
                    dependencies_satisfied = False
                    break
            if dependencies_satisfied:
                self._schedule_task(activity_task, self.task["events"][0])

        # Complete workflow
        tasks_complete = True
        for events in self._activity_task_events.values():
            if not events or events[-1]["eventType"] != "ActivityTaskCompleted":
                tasks_complete = False
                break

        if tasks_complete:
            result = {}
            for activity_id, events in self._activity_task_events.items():
                assert events and events[-1]["eventType"] == "ActivityTaskCompleted"
                attrs = events[-1].get("activityTaskCompletedEventAttributes")
                if attrs and "result" in attrs:
                    result[activity_id] = json.loads(attrs["result"])

            decision = {"decisionType": "CompleteWorkflowExecution"}
            if result:
                decision_attrs = {"result": json.dumps(result)}
                decision["completeWorkflowExecutionDecisionAttributes"] = decision_attrs
            self.decisions = [decision]
            return True

    def _process_activity_task_failed_event(self, event: t.Dict[str, t.Any]):
        attr = self._scheduled[event["eventId"]]["activityTaskScheduledEventAttributes"]
        decision_attrs = {
            "reason": "activityFailure",
            "details": "Activity '%s' failed" % attr["activityId"],
        }
        decision = {
            "decisionType": "FailWorkflowExecution",
            "failWorkflowExecutionDecisionAttributes": decision_attrs,
        }
        self.decisions = [decision]

    def _process_activity_task_timed_out_event(self, event: t.Dict[str, t.Any]):
        attr = self._scheduled[event["eventId"]]["activityTaskScheduledEventAttributes"]
        decision_attrs = {
            "reason": "activityTimeOut",
            "details": "Activity '%s' timed-out" % attr["activityId"],
        }
        decision = {
            "decisionType": "FailWorkflowExecution",
            "failWorkflowExecutionDecisionAttributes": decision_attrs,
        }
        self.decisions = [decision]

    def _process_cancel_requested_event(self):
        # Cancel running activity tasks
        running_event_types = ("ActivityTaskScheduled", "ActivityTaskStarted")
        decisions = []
        for activity_task in self.workflow.task_specs:
            events = self._activity_task_events[activity_task["id"]]
            if events and events[-1]["eventType"] in running_event_types:
                decision_attrs = {"activityId": activity_task["id"]}
                decision = {
                    "decisionType": "RequestCancelActivityTask",
                    "requestCancelActivityTaskDecisionAttributes": decision_attrs,
                }
                decisions.append(decision)

        # Cancel workflow
        decisions.append({"decisionType": "CancelWorkflowExecution"})
        self.decisions = decisions

    def _process_workflow_execution_started_event(self, event: t.Dict[str, t.Any]):
        assert event is self.task["events"][0]
        for activity_task in self.workflow.task_specs:
            assert not self._activity_task_events[activity_task["id"]]
            if not activity_task.get("dependencies"):
                self._schedule_task(activity_task, event)

    def _process_new_events(self):
        # Get new events
        event_ids = [event["eventId"] for event in self.task["events"]]
        current_idx = event_ids.index(self.task["startedEventId"])
        previous_idx = -1
        if self.task["previousStartedEventId"] in event_ids:
            previous_idx = event_ids.index(self.task["previousStartedEventId"])
        events = self.task["events"][previous_idx + 1 : current_idx + 1]
        logger.debug("Processing %d events from event %d", len(events), current_idx)

        # Process events
        assert self.task["events"][-1]["eventType"] == "DecisionTaskStarted"
        assert self.task["events"][-2]["eventType"] == "DecisionTaskScheduled"
        for event in events[:-2]:
            if event["eventType"] == "ActivityTaskCompleted":
                if self._process_activity_task_completed_event(event):
                    break
            elif event["eventType"] == "ActivityTaskFailed":
                self._process_activity_task_failed_event(event)
                break
            elif event["eventType"] == "ActivityTaskTimedOut":
                self._process_activity_task_timed_out_event(event)
                break
            elif event["eventType"] == "WorkflowExecutionCancelRequested":
                self._process_cancel_requested_event()
                break
            elif event["eventType"] == "WorkflowExecutionStarted":
                self._process_workflow_execution_started_event(event)

    def build_decisions(self):
        self._get_scheduled_references()
        self._get_activity_task_events()
        self._process_new_events()


class DAGWorkflow(_base.Workflow):
    """Dag-type SWF workflow specification.

    Args:
        name: workflow name
        version: workflow version
        task_specs: DAG task specifications
    """

    spec_type = "dag"
    decisions_builder = DAGBuilder

    def __init__(
        self, name, version, task_specs: t.List[t.Dict[str, t.Any]], description=None
    ):
        super().__init__(name, version, description)
        self.task_specs = task_specs
        self.dependants = {}

    @classmethod
    def from_spec(cls, spec):
        return cls(
            spec["name"], spec["version"], spec["tasks"], spec.get("description")
        )

    def _build_dependants(self):
        for activity_task in self.task_specs:
            dependants_task = []
            for other_activity_task in self.task_specs:
                if activity_task["id"] in other_activity_task.get("dependencies", []):
                    dependants_task.append(other_activity_task["id"])
            self.dependants[activity_task["id"]] = dependants_task

    def setup(self):
        self._build_dependants()

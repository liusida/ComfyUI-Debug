import { api } from '../../scripts/api.js';
import { app } from '../../scripts/app.js'; // Assuming `app` exports the current application instance

// Function to update STRING widget's content based on server response
function updateStringWidgetContent(nodeId, widgetName, newContent) {
    const node = app.graph._nodes.find(n => n.id === nodeId);
    if (!node) {
        console.error('Node not found:', nodeId);
        return;
    }

    const widget = node.widgets.find(w => w.name === widgetName && w.type === 'customtext');
    if (!widget) {
        console.error('STRING widget not found:', widgetName);
        return;
    }

    widget.value = newContent;
    // Optionally, if there's a callback function defined for the widget, call it
    if (widget.callback) {
        widget.callback(newContent);
    }
}

// Listen for a specific event from the server indicating a script execution is completed
api.addEventListener('executed', event => {
    const detail = event.detail;

    // Check if `output` exists and has a `string_field`
    if (detail.output && Array.isArray(detail.output.string_field)) {
        // Join the array elements into a string
        const content = detail.output.string_field.join('');

        // Example node ID and widget name, replace with actual ones
        const nodeId = parseInt(app.runningNodeId); // Replace with actual node ID
        const widgetName = 'string_field'; // Replace with actual widget name

        updateStringWidgetContent(nodeId, widgetName, content);
    } else {
        console.error('Unexpected detail format:', detail);
    }

});

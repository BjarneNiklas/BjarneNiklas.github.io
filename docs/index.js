const iface = gr.Interface.autoLoad({
    element: "#interface",
    model: window.model,
    inputs: gr.textbox(),
    outputs: gr.textbox(),
    live: true,
    theme: 'compact',
    title: 'LSTM Wortvorhersage'
});
require "webdnn"

const cdnHost = "https://raw.githubusercontent.com/webdnnModels/fast-neural-style-transfer/master/"
    const options = {backendOrder:['webgpu','webassembly','webgl']}
    const dnn
    dnn = await WebDNN.load(`${cdnHost}output.candy`, options)
    // dnn = await WebDNN.load(`${cdnHost}output.fur`, options)
    // dnn = await WebDNN.load(`${cdnHost}output.kanagawa`, options)
    // dnn = await WebDNN.load(`${cdnHost}output.kandinsky`, options)
    // dnn = await WebDNN.load(`${cdnHost}output.scream`, options)
    // dnn = await WebDNN.load(`${cdnHost}output.starrynight`, options)

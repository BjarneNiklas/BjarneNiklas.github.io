const canvas = document.getElementById('glCanvas');
const gl = canvas.getContext('webgl');

if (!gl) {
    alert('WebGL is not supported in your browser.');
}

const vsSource = `
    attribute vec2 aPosition;
    void main(void) {
        gl_Position = vec4(aPosition, 0.0, 1.0);
    }
`;

const fsSource = `
    void main(void) {
        gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0); // Black color
    }
`;

function compileShader(gl, sourceCode, type) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, sourceCode);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        console.error('Error compiling shader:', gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
        return null;
    }
    return shader;
}

const vertexShader = compileShader(gl, vsSource, gl.VERTEX_SHADER);
const fragmentShader = compileShader(gl, fsSource, gl.FRAGMENT_SHADER);

const shaderProgram = gl.createProgram();
gl.attachShader(shaderProgram, vertexShader);
gl.attachShader(shaderProgram, fragmentShader);
gl.linkProgram(shaderProgram);

if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
    console.error('Error linking program:', gl.getProgramInfoLog(shaderProgram));
}

gl.useProgram(shaderProgram);

const vertices = new Float32Array([
    // Radial lines
    0.0,  0.0,   // Center
    0.0,  0.5,   // Top
    0.0,  0.0,   // Center
    0.35, 0.35,  // Top-right
    0.0,  0.0,   // Center
    0.5,  0.0,   // Right
    0.0,  0.0,   // Center
    0.35, -0.35, // Bottom-right
    0.0,  0.0,   // Center
    0.0,  -0.5,  // Bottom
    0.0,  0.0,   // Center
    -0.35, -0.35,// Bottom-left
    0.0,  0.0,   // Center
    -0.5, 0.0,   // Left
    0.0,  0.0,   // Center
    -0.35, 0.35, // Top-left

    // Outer circle
    0.0,  0.5,   // Top
    0.35, 0.35,  // Top-right
    0.5,  0.0,   // Right
    0.35, -0.35, // Bottom-right
    0.0,  -0.5,  // Bottom
    -0.35, -0.35,// Bottom-left
    -0.5, 0.0,   // Left
    -0.35, 0.35, // Top-left

    // Middle circle
    0.0,  0.375,   // Top
    0.262, 0.262,  // Top-right
    0.375, 0.0,   // Right
    0.262, -0.262, // Bottom-right
    0.0,  -0.375,  // Bottom
    -0.262, -0.262,// Bottom-left
    -0.375, 0.0,   // Left
    -0.262, 0.262, // Top-left

    // Inner circle (smaller octagon)
    0.0,  0.25,  // Top
    0.18, 0.18,  // Top-right
    0.25, 0.0,   // Right
    0.18, -0.18, // Bottom-right
    0.0,  -0.25, // Bottom
    -0.18, -0.18,// Bottom-left
    -0.25, 0.0,  // Left
    -0.18, 0.18,  // Top-left

    // Inner circle (smallest octagon)
    0.0,  0.125,  // Top
    0.09, 0.09,  // Top-right
    0.125, 0.0,   // Right
    0.09, -0.09, // Bottom-right
    0.0,  -0.125, // Bottom
    -0.09, -0.09,// Bottom-left
    -0.125, 0.0,  // Left
    -0.09, 0.09  // Top-left
]);

const vertexBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);

const positionAttributeLocation = gl.getAttribLocation(shaderProgram, 'aPosition');
gl.enableVertexAttribArray(positionAttributeLocation);
gl.vertexAttribPointer(positionAttributeLocation, 2, gl.FLOAT, false, 0, 0);

// Clear canvas and set background color
gl.clearColor(1.0, 1.0, 1.0, 1.0); // White background
gl.clear(gl.COLOR_BUFFER_BIT);

// Draw the radial lines
gl.lineWidth(2.0);
gl.drawArrays(gl.LINES, 0, 16);

// Draw circles
gl.drawArrays(gl.LINE_LOOP, 16, 8);
gl.drawArrays(gl.LINE_LOOP, 24, 8);
gl.drawArrays(gl.LINE_LOOP, 32, 8);
gl.drawArrays(gl.LINE_LOOP, 40, 8); 

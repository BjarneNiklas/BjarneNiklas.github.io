let scene, camera, renderer;
let points = [];
let tsne;
let stepCount = 0;
const colorMap = {1: 0xff0000, 2: 0x00ff00, 3: 0x0000ff};

async function loadData() {
    const response = await fetch('Seeds_dataset.csv');
    const text = await response.text();
    const data = text.trim().split('\n').map(row => row.split(',').map(Number));
    return data;
}

function initTSNE(data) {
    tsne = new tsnejs.tSNE({
        dim: 3,
        perplexity: 30,
        learningRate: 200,
        iterations: 1000,
    });
    tsne.initDataRaw(data.map(d => d.slice(0, 7)));
}

function init3DScene() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);
    
    camera.position.set(0, 0, 10);
}

function addPoints(data) {
    data.forEach((point, index) => {
        const geometry = new THREE.SphereGeometry(0.1, 8, 8);
        const material = new THREE.MeshBasicMaterial({color: colorMap[point[7]]}); // Klassenfarbe
        const sphere = new THREE.Mesh(geometry, material);
        sphere.position.set(point[0], point[1], point[2]);
        scene.add(sphere);
        points.push(sphere);
    });
}

function updateVisualization() {
    const solution = tsne.getSolution();
    points.forEach((point, index) => {
        point.position.set(solution[index][0], solution[index][1], solution[index][2]);
    });
    renderer.render(scene, camera);
}

document.getElementById("restart-btn").addEventListener("click", () => {
    iterateTSNE();
});

// Schrittweise t-SNE durchführen
function iterateTSNE() {
    tsne.step();
    stepCount++;
    document.getElementById("step-count").textContent = `Step-Count: ${stepCount}`;
    updateVisualization();
}

function handleKeyPress(event) {
    const moveDistance = 0.1;
    const rotateAngle = 0.05;

    switch (event.key) {
        case 'w': 
            camera.position.z -= moveDistance;
            break;
        case 's': 
            camera.position.z += moveDistance;
            break;
        case 'a': 
            camera.position.x -= moveDistance;
            break;
        case 'd': 
            camera.position.x += moveDistance;
            break;
        case 'ArrowUp':
            scene.rotation.x += rotateAngle;
            break;
        case 'ArrowDown':
            scene.rotation.x -= rotateAngle;
            break;
        case 'ArrowLeft': 
            scene.rotation.y += rotateAngle;
            break;
        case 'ArrowRight': 
            scene.rotation.y -= rotateAngle;
            break;
    }
    updateVisualization();
}

async function main() {
    const data = await loadData();
    init3DScene();
    initTSNE(data);
    addPoints(data);
    updateVisualization();
    
    document.addEventListener("keypress", (e) => {
        if (e.key.toUpperCase() === "T") {
            iterateTSNE();
        }
    });
    document.addEventListener("keydown", handleKeyPress);
}

main();

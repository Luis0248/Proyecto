
let map, markerResidencia, markerTrabajo;
let latResidencia, lonResidencia, latTrabajo, lonTrabajo;

function initMap() {
    map = L.map('map').setView([4.60971, -74.08175], 12);

    // Agrega la capa de mapa de OpenStreetMap
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    // Configuración del marcador de residencia
    markerResidencia = L.marker([4.60971, -74.08175], { draggable: true })
        .addTo(map)
        .bindPopup("Residencia")
        .openPopup();
    markerResidencia.on('dragend', function (e) {
        const position = markerResidencia.getLatLng();
        latResidencia = position.lat;
        lonResidencia = position.lng;
    });

    // Configuración del marcador de trabajo
    markerTrabajo = L.marker([4.60971, -74.08175], { draggable: true })
        .addTo(map)
        .bindPopup("Trabajo");
    markerTrabajo.on('dragend', function (e) {
        const position = markerTrabajo.getLatLng();
        latTrabajo = position.lat;
        lonTrabajo = position.lng;
    });
}

initMap();

// Enviar datos del formulario
document.getElementById('formEstudiante').addEventListener('submit', function (event) {
    event.preventDefault();
    const cedula = document.getElementById('cedula').value;
    const nombres = document.getElementById('nombres').value;
    const apellidos = document.getElementById('apellidos').value;
    const direccionResidencia = document.getElementById('direccion_residencia').value;
    const direccionTrabajo = document.getElementById('direccion_trabajo').value;

    const data = {
        cedula,
        nombres,
        apellidos,
        direccion_residencia: direccionResidencia,
        lat_residencia: latResidencia,
        lon_residencia: lonResidencia,
        direccion_trabajo: direccionTrabajo,
        lat_trabajo: latTrabajo,
        lon_trabajo: lonTrabajo
    };

    fetch('http://localhost:5000/estudiantes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error:', error));
});


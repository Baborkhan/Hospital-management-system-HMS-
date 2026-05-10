let map;
let marker;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 23.8103, lng: 90.4125 }, // Dhaka
        zoom: 12,
    });
}

window.initMap = initMap;

// Current location
document.getElementById("currentLocationBtn").addEventListener("click", () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
            };
            map.setCenter(pos);
            if (marker) marker.setMap(null);
            marker = new google.maps.Marker({ position: pos, map: map });
        });
    } else {
        alert("Geolocation not supported by your browser");
    }
});

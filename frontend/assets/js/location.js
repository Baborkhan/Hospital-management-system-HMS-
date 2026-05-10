// ===== LOCATION MANAGEMENT =====

const locationData = {
    dhaka: [
        "Gulshan", "Banani", "Dhanmondi", "Mirpur", "Uttara",
        "Motijheel", "Farmgate", "Mohakhali", "Bashundhara", "Mohammadpur"
    ],
    chittagong: [
        "Agrabad", "GEC Circle", "Khatunganj", "Halishahar",
        "Bayezid", "Nasirabad", "Panchlaish", "Chawkbazar"
    ],
    sylhet: [
        "Zindabazar", "Amberkhana", "Mirabazar", "Shahi Eidgah",
        "Kumarpara", "Subhanighat", "Osmani Nagar", "Bandar Bazar"
    ],
    rajshahi: [
        "Shaheb Bazar", "Kazla", "Motihar", "Binodpur",
        "Seroil", "Boat Ghat", "Alupatti", "RDA Road"
    ],
    khulna: [
        "Sonadanga", "Khalishpur", "Daulatpur", "Khan Jahan Ali",
        "Boyra", "Rupsha", "Labonchora", "Gollamari"
    ]
};

const areaDetails = {
    gulshan: { lat: 23.7947, lng: 90.4145 },
    banani: { lat: 23.7940, lng: 90.4075 },
    dhanmondi: { lat: 23.7400, lng: 90.3650 },
    mirpur: { lat: 23.8223, lng: 90.3654 },
    uttara: { lat: 23.8759, lng: 90.3795 }
};

document.addEventListener('DOMContentLoaded', function() {
    initLocationSelectors();
    initGeolocation();
    initMapView();
});

// ===== LOCATION SELECTORS =====
function initLocationSelectors() {
    const citySelect = document.getElementById('citySelect');
    const areaSelect = document.getElementById('areaSelect');
    
    if (!citySelect) return;
    
    // City change event
    citySelect.addEventListener('change', function() {
        const selectedCity = this.value;
        updateAreaDropdown(selectedCity);
        
        // Save selected city
        localStorage.setItem('medfind_selected_city', selectedCity);
        
        // Trigger city change event
        document.dispatchEvent(new CustomEvent('cityChanged', {
            detail: { city: selectedCity }
        }));
    });
    
    // Area change event
    if (areaSelect) {
        areaSelect.addEventListener('change', function() {
            const selectedArea = this.value;
            if (selectedArea) {
                localStorage.setItem('medfind_selected_area', selectedArea);
                
                document.dispatchEvent(new CustomEvent('areaChanged', {
                    detail: { area: selectedArea }
                }));
            }
        });
    }
    
    // Load saved location
    loadSavedLocation();
}

function updateAreaDropdown(city) {
    const areaSelect = document.getElementById('areaSelect');
    if (!areaSelect) return;
    
    // Clear existing options
    areaSelect.innerHTML = '<option value="">Select Area</option>';
    areaSelect.disabled = true;
    
    if (city && locationData[city]) {
        // Enable area select
        areaSelect.disabled = false;
        
        // Add areas
        locationData[city].forEach(area => {
            const option = document.createElement('option');
            option.value = area.toLowerCase();
            option.textContent = area;
            areaSelect.appendChild(option);
        });
        
        // Add animation
        areaSelect.classList.add('animate-fade-in');
        setTimeout(() => {
            areaSelect.classList.remove('animate-fade-in');
        }, 500);
        
        // Load saved area for this city
        const savedArea = localStorage.getItem('medfind_selected_area');
        if (savedArea && locationData[city].includes(
            savedArea.charAt(0).toUpperCase() + savedArea.slice(1)
        )) {
            areaSelect.value = savedArea;
        }
    }
}

function loadSavedLocation() {
    const citySelect = document.getElementById('citySelect');
    const areaSelect = document.getElementById('areaSelect');
    
    if (!citySelect) return;
    
    // Load saved city
    const savedCity = localStorage.getItem('medfind_selected_city');
    if (savedCity && locationData[savedCity]) {
        citySelect.value = savedCity;
        citySelect.dispatchEvent(new Event('change'));
    }
    
    // Load saved area
    if (areaSelect) {
        const savedArea = localStorage.getItem('medfind_selected_area');
        if (savedArea) {
            setTimeout(() => {
                areaSelect.value = savedArea;
            }, 100);
        }
    }
}

// ===== GEOLOCATION =====
function initGeolocation() {
    const geolocationBtn = document.getElementById('geolocationBtn');
    
    if (geolocationBtn) {
        geolocationBtn.addEventListener('click', function() {
            if (navigator.geolocation) {
                showNotification('Detecting your location...', 'info');
                
                navigator.geolocation.getCurrentPosition(
                    // Success callback
                    function(position) {
                        const lat = position.coords.latitude;
                        const lng = position.coords.longitude;
                        
                        // Reverse geocode (in production, use a proper geocoding service)
                        const nearestCity = getNearestCity(lat, lng);
                        
                        if (nearestCity) {
                            updateLocationFromGeolocation(nearestCity);
                            showNotification(`Location set to ${nearestCity}`, 'success');
                        } else {
                            showNotification('Could not determine your city', 'warning');
                        }
                    },
                    // Error callback
                    function(error) {
                        handleGeolocationError(error);
                    },
                    // Options
                    {
                        enableHighAccuracy: true,
                        timeout: 5000,
                        maximumAge: 0
                    }
                );
            } else {
                showNotification('Geolocation is not supported by your browser', 'error');
            }
        });
    }
}

function getNearestCity(lat, lng) {
    // Simple city detection (in production, use a proper reverse geocoding API)
    const cityCoordinates = {
        dhaka: { lat: 23.8103, lng: 90.4125 },
        chittagong: { lat: 22.3569, lng: 91.7832 },
        sylhet: { lat: 24.8949, lng: 91.8687 },
        rajshahi: { lat: 24.3745, lng: 88.6042 },
        khulna: { lat: 22.8456, lng: 89.5403 }
    };
    
    let nearestCity = null;
    let minDistance = Infinity;
    
    for (const [city, coords] of Object.entries(cityCoordinates)) {
        const distance = calculateDistance(lat, lng, coords.lat, coords.lng);
        if (distance < minDistance) {
            minDistance = distance;
            nearestCity = city;
        }
    }
    
    return nearestCity;
}

function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Earth's radius in kilometers
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

function updateLocationFromGeolocation(city) {
    const citySelect = document.getElementById('citySelect');
    if (citySelect && locationData[city]) {
        citySelect.value = city;
        citySelect.dispatchEvent(new Event('change'));
        
        // Save to localStorage
        localStorage.setItem('medfind_geolocation_city', city);
        localStorage.setItem('medfind_last_location_source', 'geolocation');
    }
}

function handleGeolocationError(error) {
    let message = 'Unable to retrieve your location. ';
    
    switch(error.code) {
        case error.PERMISSION_DENIED:
            message += 'Please enable location permissions in your browser settings.';
            break;
        case error.POSITION_UNAVAILABLE:
            message += 'Location information is unavailable.';
            break;
        case error.TIMEOUT:
            message += 'The request to get your location timed out.';
            break;
        default:
            message += 'An unknown error occurred.';
    }
    
    showNotification(message, 'error');
}

// ===== MAP VIEW =====
function initMapView() {
    const mapBtn = document.querySelector('.map-btn');
    
    if (mapBtn) {
        mapBtn.addEventListener('click', function() {
            const citySelect = document.getElementById('citySelect');
            const areaSelect = document.getElementById('areaSelect');
            
            const city = citySelect ? citySelect.value : null;
            const area = areaSelect ? areaSelect.value : null;
            
            if (city && area) {
                openMapView(city, area);
            } else {
                showNotification('Please select both city and area first', 'warning');
            }
        });
    }
}

function openMapView(city, area) {
    // In production, this would open a modal with Google Maps/Leaflet
    // For now, show a notification and simulate map view
    
    showNotification(`Opening map view for ${area}, ${city}`, 'info');
    
    // Create map modal
    const modal = document.createElement('div');
    modal.id = 'map-modal';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease-out;
    `;
    
    modal.innerHTML = `
        <div style="background: white; border-radius: 12px; width: 90%; max-width: 800px; max-height: 90vh; overflow: hidden;">
            <div style="padding: 20px; border-bottom: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; color: #111827;">
                    <i class="fas fa-map-marker-alt" style="color: #ef4444; margin-right: 10px;"></i>
                    Hospitals in ${area}, ${city}
                </h3>
                <button id="close-map" style="background: none; border: none; font-size: 24px; cursor: pointer; color: #6b7280;">&times;</button>
            </div>
            <div style="padding: 20px; text-align: center;">
                <div style="background: #f3f4f6; border-radius: 8px; height: 400px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
                    <div>
                        <i class="fas fa-map" style="font-size: 64px; color: #9ca3af; margin-bottom: 20px;"></i>
                        <p style="color: #6b7280;">Map view would show here</p>
                        <p style="color: #9ca3af; font-size: 14px;">(In production: Google Maps/Leaflet integration)</p>
                    </div>
                </div>
                <div style="display: flex; gap: 10px; justify-content: center;">
                    <button class="btn btn-primary" onclick="openInGoogleMaps('${city}', '${area}')">
                        <i class="fab fa-google"></i> Open in Google Maps
                    </button>
                    <button class="btn btn-secondary" onclick="closeMapView()">
                        Close
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';
    
    // Close button event
    const closeBtn = document.getElementById('close-map');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeMapView);
    }
    
    // Close on outside click
    modal.addEventListener('click', function(e) {
        if (e.target === this) {
            closeMapView();
        }
    });
    
    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeMapView();
        }
    });
}

function closeMapView() {
    const modal = document.getElementById('map-modal');
    if (modal) {
        modal.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => {
            if (modal.parentNode) {
                modal.parentNode.removeChild(modal);
            }
            document.body.style.overflow = '';
        }, 300);
    }
}

function openInGoogleMaps(city, area) {
    const query = encodeURIComponent(`${area}, ${city}, Bangladesh`);
    window.open(`https://www.google.com/maps/search/hospitals+${query}`, '_blank');
}

// ===== LOCATION UTILITIES =====
function getCurrentLocation() {
    return {
        city: localStorage.getItem('medfind_selected_city'),
        area: localStorage.getItem('medfind_selected_area'),
        source: localStorage.getItem('medfind_last_location_source')
    };
}

function setLocation(city, area) {
    const citySelect = document.getElementById('citySelect');
    const areaSelect = document.getElementById('areaSelect');
    
    if (citySelect && locationData[city]) {
        citySelect.value = city;
        citySelect.dispatchEvent(new Event('change'));
        
        setTimeout(() => {
            if (areaSelect && area) {
                areaSelect.value = area;
                areaSelect.dispatchEvent(new Event('change'));
            }
        }, 100);
        
        return true;
    }
    
    return false;
}

function clearLocation() {
    localStorage.removeItem('medfind_selected_city');
    localStorage.removeItem('medfind_selected_area');
    
    const citySelect = document.getElementById('citySelect');
    const areaSelect = document.getElementById('areaSelect');
    
    if (citySelect) {
        citySelect.value = '';
        citySelect.dispatchEvent(new Event('change'));
    }
    
    if (areaSelect) {
        areaSelect.innerHTML = '<option value="">Select Area</option>';
        areaSelect.disabled = true;
        areaSelect.value = '';
    }
    
    showNotification('Location cleared', 'info');
}

// ===== EXPORT FUNCTIONS =====
window.getCurrentLocation = getCurrentLocation;
window.setLocation = setLocation;
window.clearLocation = clearLocation;
window.openInGoogleMaps = openInGoogleMaps;
const locations = {
    Dhaka: ["Gulshan", "Banani", "Mirpur", "Dhanmondi"],
    Chattogram: ["Pahartali", "Agrabad", "Panchlaish"],
    Rajshahi: ["Boalia", "Motihar"],
    Khulna: ["Sonadanga", "Khalishpur"],
};

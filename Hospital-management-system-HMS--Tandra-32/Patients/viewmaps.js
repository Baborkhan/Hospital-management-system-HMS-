document.addEventListener('DOMContentLoaded', function() {
  // DOM Elements
  const divisions = document.querySelectorAll('.division');
  const divisionBtns = document.querySelectorAll('.division-btn');
  const tooltip = document.getElementById('map-tooltip');
  const searchInput = document.getElementById('searchInput');
  const searchBtn = document.getElementById('searchBtn');
  const selectedDivisionElement = document.getElementById('selected-division');
  const hospitalCountElement = document.getElementById('hospital-count');
  const hospitalsGrid = document.getElementById('hospitalsGrid');
  const hospitalSearch = document.getElementById('hospitalSearch');
  const hospitalType = document.getElementById('hospitalType');
  const filterBtn = document.querySelector('.filter-btn');

  // Hospital data with exactly 10 selected hospitals for each division
  const hospitalData = {
    'Rajshahi': generateHospitalData('Rajshahi', 10),
    'Dhaka': generateHospitalData('Dhaka', 10),
    'Chittagong': generateHospitalData('Chittagong', 10),
    'Khulna': generateHospitalData('Khulna', 10),
    'Sylhet': generateHospitalData('Sylhet', 10),
    'Barisal': generateHospitalData('Barisal', 10),
    'Rangpur': generateHospitalData('Rangpur', 10),
    'Mymensingh': generateHospitalData('Mymensingh', 10)
  };

  // Initialize
  selectDivision('Rajshahi');

  // Map division hover effects
  divisions.forEach(div => {
    div.addEventListener('mouseenter', function(e) {
      const divisionName = this.id;
      const totalHospitals = this.getAttribute('data-hospitals');
      const selectedHospitals = this.getAttribute('data-selected');
      const otherHospitals = this.getAttribute('data-other');
      
      tooltip.innerHTML = `
        <div style="font-weight: 700; font-size: 16px; margin-bottom: 5px; color: #4caf50;">${divisionName} Division</div>
        <div style="margin-bottom: 8px; color: #546e7a;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
            <span>Selected Hospitals:</span>
            <span style="color: #4caf50; font-weight: 600;">${selectedHospitals}</span>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
            <span>Other Hospitals:</span>
            <span style="color: #2196f3; font-weight: 600;">${otherHospitals}</span>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span>Total Hospitals:</span>
            <span style="color: #ff9800; font-weight: 600;">${totalHospitals}</span>
          </div>
        </div>
        <div style="margin-top: 10px; font-size: 12px; color: #90a4ae; text-align: center;">
          Click to view details →
        </div>
      `;
      
      // Position tooltip
      const rect = this.getBoundingClientRect();
      const mapContainer = document.querySelector('.map-container');
      const mapRect = mapContainer.getBoundingClientRect();
      
      let x = e.clientX - mapRect.left + 15;
      let y = e.clientY - mapRect.top + 15;
      
      // Keep tooltip within map bounds
      if (x > mapRect.width - 250) x = mapRect.width - 250;
      if (y > mapRect.height - 150) y = mapRect.height - 150;
      
      tooltip.style.left = x + 'px';
      tooltip.style.top = y + 'px';
      tooltip.style.opacity = '1';
    });
    
    div.addEventListener('mousemove', function(e) {
      const mapContainer = document.querySelector('.map-container');
      const mapRect = mapContainer.getBoundingClientRect();
      
      let x = e.clientX - mapRect.left + 15;
      let y = e.clientY - mapRect.top + 15;
      
      if (x > mapRect.width - 250) x = mapRect.width - 250;
      if (y > mapRect.height - 150) y = mapRect.height - 150;
      
      tooltip.style.left = x + 'px';
      tooltip.style.top = y + 'px';
    });
    
    div.addEventListener('mouseleave', function() {
      tooltip.style.opacity = '0';
    });
    
    div.addEventListener('click', function() {
      selectDivision(this.id);
      
      // Scroll to hospitals section smoothly
      document.querySelector('.hospitals-section').scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
      });
    });
  });

  // Division buttons click
  divisionBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      const divisionName = this.getAttribute('data-division');
      selectDivision(divisionName);
      
      // Scroll to hospitals section
      document.querySelector('.hospitals-section').scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
      });
    });
  });

  // Search functionality
  searchBtn.addEventListener('click', performSearch);
  searchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') performSearch();
  });

  // Hospital search filter
  filterBtn.addEventListener('click', filterHospitals);
  hospitalSearch.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') filterHospitals();
  });
  hospitalType.addEventListener('change', filterHospitals);

  function selectDivision(divisionName) {
    // Update active states on map
    divisions.forEach(div => {
      div.classList.remove('active');
      if (div.id === divisionName) {
        div.classList.add('active');
      }
    });
    
    // Update active button
    divisionBtns.forEach(btn => {
      btn.classList.remove('active');
      if (btn.getAttribute('data-division') === divisionName) {
        btn.classList.add('active');
      }
    });
    
    // Update labels
    document.querySelectorAll('.division-label').forEach(label => {
      label.classList.remove('active');
    });
    
    document.querySelectorAll('.hospital-count').forEach(count => {
      count.classList.remove('active');
    });
    
    // Update selected division
    selectedDivisionElement.textContent = divisionName;
    
    // Display hospitals
    displayHospitals(divisionName);
  }

  function performSearch() {
    const searchTerm = searchInput.value.trim().toLowerCase();
    
    if (!searchTerm) {
      alert('Please enter a division name to search');
      return;
    }
    
    // Find matching division
    let matchedDivision = null;
    divisionBtns.forEach(btn => {
      const divisionName = btn.getAttribute('data-division').toLowerCase();
      if (divisionName.includes(searchTerm)) {
        matchedDivision = btn.getAttribute('data-division');
      }
    });
    
    if (matchedDivision) {
      selectDivision(matchedDivision);
    } else {
      alert(`No division found for "${searchInput.value}". Try: Rajshahi, Dhaka, Chittagong, etc.`);
    }
  }

  function displayHospitals(divisionName) {
    const hospitals = hospitalData[divisionName] || [];
    hospitalCountElement.textContent = hospitals.length;
    
    let html = '';
    
    if (hospitals.length === 0) {
      html = `
        <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; background: #f8fafc; border-radius: 10px;">
          <i class="fas fa-hospital" style="font-size: 4rem; color: #bbdefb; margin-bottom: 20px;"></i>
          <h3 style="color: #546e7a; margin-bottom: 10px;">No Hospitals Found</h3>
          <p style="color: #90a4ae; max-width: 400px; margin: 0 auto;">
            Hospital data for ${divisionName} division is being updated.
          </p>
        </div>
      `;
    } else {
      hospitals.forEach(hospital => {
        const typeClass = hospital.type || 'private';
        
        html += `
          <div class="hospital-card">
            <div class="hospital-header">
              <div class="hospital-icon">
                <i class="${hospital.icon}"></i>
              </div>
              <div class="hospital-info">
                <h3>${hospital.name}</h3>
                <span class="hospital-type ${typeClass}">
                  ${typeClass.charAt(0).toUpperCase() + typeClass.slice(1)} Hospital
                </span>
                <div class="hospital-address">
                  <i class="fas fa-map-marker-alt"></i>
                  <span>${hospital.address}</span>
                </div>
              </div>
            </div>
            
            <div class="hospital-details">
              <div class="detail-item">
                <i class="fas fa-phone"></i>
                <span>${hospital.phone}</span>
              </div>
              <div class="detail-item">
                <i class="fas fa-bed"></i>
                <span>${hospital.beds} Beds</span>
              </div>
            </div>
          </div>
        `;
      });
    }
    
    hospitalsGrid.innerHTML = html;
  }

  function filterHospitals() {
    const divisionName = selectedDivisionElement.textContent;
    const hospitals = hospitalData[divisionName] || [];
    const searchTerm = hospitalSearch.value.toLowerCase();
    const typeFilter = hospitalType.value;
    
    const filteredHospitals = hospitals.filter(hospital => {
      const matchesSearch = !searchTerm || 
        hospital.name.toLowerCase().includes(searchTerm) ||
        hospital.address.toLowerCase().includes(searchTerm);
      
      const matchesType = typeFilter === 'all' || hospital.type === typeFilter;
      
      return matchesSearch && matchesType;
    });
    
    hospitalCountElement.textContent = filteredHospitals.length;
    
    let html = '';
    
    if (filteredHospitals.length === 0) {
      html = `
        <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; background: #f8fafc; border-radius: 10px;">
          <i class="fas fa-search" style="font-size: 4rem; color: #bbdefb; margin-bottom: 20px;"></i>
          <h3 style="color: #546e7a; margin-bottom: 10px;">No Hospitals Found</h3>
          <p style="color: #90a4ae; max-width: 400px; margin: 0 auto;">
            Try adjusting your search criteria
          </p>
        </div>
      `;
    } else {
      filteredHospitals.forEach(hospital => {
        const typeClass = hospital.type || 'private';
        
        html += `
          <div class="hospital-card">
            <div class="hospital-header">
              <div class="hospital-icon">
                <i class="${hospital.icon}"></i>
              </div>
              <div class="hospital-info">
                <h3>${hospital.name}</h3>
                <span class="hospital-type ${typeClass}">
                  ${typeClass.charAt(0).toUpperCase() + typeClass.slice(1)} Hospital
                </span>
                <div class="hospital-address">
                  <i class="fas fa-map-marker-alt"></i>
                  <span>${hospital.address}</span>
                </div>
              </div>
            </div>
            
            <div class="hospital-details">
              <div class="detail-item">
                <i class="fas fa-phone"></i>
                <span>${hospital.phone}</span>
              </div>
              <div class="detail-item">
                <i class="fas fa-bed"></i>
                <span>${hospital.beds} Beds</span>
              </div>
            </div>
          </div>
        `;
      });
    }
    
    hospitalsGrid.innerHTML = html;
  }

  function generateHospitalData(division, count) {
    const hospitals = [];
    const types = ['government', 'private', 'specialized'];
    const icons = ['fas fa-hospital', 'fas fa-clinic-medical', 'fas fa-stethoscope'];
    
    for (let i = 1; i <= count; i++) {
      const type = types[Math.floor(Math.random() * types.length)];
      const icon = icons[Math.floor(Math.random() * icons.length)];
      
      hospitals.push({
        name: `${division} ${type.charAt(0).toUpperCase() + type.slice(1)} Hospital ${i}`,
        type: type,
        icon: icon,
        address: `Main Road, ${division} ${i}000`,
        phone: `01${Math.floor(Math.random() * 90000000 + 10000000)}`,
        beds: Math.floor(Math.random() * 300) + 50
      });
    }
    
    return hospitals;
  }
});
// location.js

const cityAreaMap = {
    dhaka: ["Dhanmondi", "Mirpur", "Uttara"],
    rajshahi: ["Shaheb Bazar", "Kazla"],
    ishwardi: ["Rail Gate", "Hospital Road"],
    pabna: ["Pabna City", "Bhangura"]
};

const citySelect = document.getElementById("city");
const areaSelect = document.getElementById("area");

citySelect.addEventListener("change", () => {
    const city = citySelect.value;
    areaSelect.innerHTML = "";

    if (!city) {
        areaSelect.disabled = true;
        areaSelect.innerHTML = "<option>Select City First</option>";
        return;
    }

    areaSelect.disabled = false;
    cityAreaMap[city].forEach(area => {
        const opt = document.createElement("option");
        opt.value = area;
        opt.textContent = area;
        areaSelect.appendChild(opt);
    });
});

// DOM Elements
const cityInput = document.getElementById('cityInput');
const locationBtn = document.getElementById('locationBtn');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const mainWeather = document.getElementById('mainWeather');
const weatherBg = document.getElementById('weatherBg');

// Animation Elements
const rainContainer = document.getElementById('rainContainer');
const snowContainer = document.getElementById('snowContainer');
const cloudsContainer = document.getElementById('cloudsContainer');
const sunRays = document.getElementById('sunRays');
const stars = document.getElementById('stars');
const lightning = document.getElementById('lightning');

// Event Listeners
cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const city = cityInput.value.trim();
        if (city) fetchWeather(city);
    }
});

locationBtn.addEventListener('click', () => fetchWeather());

// Fetch Weather
async function fetchWeather(city = null) {
    showLoading();
    hideError();

    try {
        const currentUrl = city
            ? `/api/weather/current?city=${encodeURIComponent(city)}`
            : '/api/weather/current';

        const forecastUrl = city
            ? `/api/weather/forecast?city=${encodeURIComponent(city)}`
            : '/api/weather/forecast';

        const [currentResponse, forecastResponse] = await Promise.all([
            fetch(currentUrl),
            fetch(forecastUrl)
        ]);

        if (!currentResponse.ok) throw new Error('Unable to fetch weather data');

        const currentData = await currentResponse.json();
        const forecastData = await forecastResponse.json();

        displayCurrentWeather(currentData);
        displayForecast(forecastData);
        generateHourlyForecast();
        updateWeatherAnimations(currentData.description);

        hideLoading();

    } catch (err) {
        hideLoading();
        showError(err.message || 'Something went wrong. Please try again.');
    }
}

// Display Current Weather
function displayCurrentWeather(data) {
    document.getElementById('cityName').textContent = `${data.city}, ${data.country}`;
    document.getElementById('currentTime').textContent = new Date().toLocaleString('en-US', {
        weekday: 'long',
        hour: '2-digit',
        minute: '2-digit'
    });

    document.getElementById('mainWeatherIcon').src = data.icon_url;
    document.getElementById('mainTemperature').textContent = data.temperature;
    document.getElementById('mainCondition').textContent = data.description;
    document.getElementById('feelsLike').textContent = data.feels_like;

    document.getElementById('tempMax').textContent = data.temperature + 2;
    document.getElementById('tempMin').textContent = data.temperature - 2;

    document.getElementById('windSpeed').textContent = `${data.wind_speed} km/h`;
    document.getElementById('humidity').textContent = `${data.humidity}%`;
    document.getElementById('pressure').textContent = `${data.pressure} hPa`;
    document.getElementById('visibility').textContent = `${data.visibility} km`;

    document.getElementById('sunrise').textContent = data.sunrise;
    document.getElementById('sunset').textContent = data.sunset;

    mainWeather.classList.remove('hidden');
}

// Generate Hourly Forecast
function generateHourlyForecast() {
    const container = document.getElementById('hourlyContainer');
    container.innerHTML = '';

    const hours = ['Now', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM'];
    const currentTemp = parseInt(document.getElementById('mainTemperature').textContent);

    hours.forEach((hour, index) => {
        const temp = currentTemp + Math.floor(Math.random() * 5 - 2);
        const item = document.createElement('div');
        item.className = 'hourly-item';
        item.innerHTML = `
            <p class="hourly-time">${hour}</p>
            <img src="${document.getElementById('mainWeatherIcon').src}" class="hourly-icon" alt="weather">
            <p class="hourly-temp">${temp}°</p>
            <p class="hourly-desc">${index % 3 === 0 ? 'Clear' : index % 2 === 0 ? 'Cloudy' : 'Partly'}</p>
        `;
        container.appendChild(item);
    });
}

// Display Forecast
function displayForecast(data) {
    const container = document.getElementById('forecastGrid');
    container.innerHTML = '';

    data.forEach(day => {
        const card = document.createElement('div');
        card.className = 'forecast-card';
        card.innerHTML = `
            <p class="forecast-date">${day.date}</p>
            <img src="${day.icon_url}" class="forecast-icon" alt="${day.description}">
            <p class="forecast-temps">${day.temp_max}° / ${day.temp_min}°</p>
            <p class="forecast-desc">${day.description}</p>
        `;
        container.appendChild(card);
    });
}

// ========================================
// WEATHER ANIMATIONS + GIF BACKGROUNDS
// ========================================

function updateWeatherAnimations(condition) {
    const conditionLower = condition.toLowerCase();
    const hour = new Date().getHours();
    const isNight = hour >= 19 || hour <= 6;

    // Reset all animations
    stopAllAnimations();

    // Remove all weather classes
    weatherBg.className = 'weather-bg';

    // Apply GIF background + animations based on weather
    if (conditionLower.includes('thunder') || conditionLower.includes('storm')) {
        weatherBg.classList.add('stormy');
        startRain();
        startLightning();
        cloudsContainer.classList.add('active');
    }
    else if (conditionLower.includes('rain') || conditionLower.includes('drizzle')) {
        weatherBg.classList.add('rainy');
        startRain();
        cloudsContainer.classList.add('active');
    }
    else if (conditionLower.includes('snow')) {
        weatherBg.classList.add('snowy');
        startSnow();
        cloudsContainer.classList.add('active');
    }
    else if (conditionLower.includes('cloud')) {
        weatherBg.classList.add('cloudy');
        cloudsContainer.classList.add('active');
    }
    else if (conditionLower.includes('mist') || conditionLower.includes('fog') || conditionLower.includes('haze')) {
        weatherBg.classList.add('mist');
        cloudsContainer.classList.add('active');
    }
    else if (conditionLower.includes('clear') || conditionLower.includes('sunny')) {
        const sunsetHours = [6, 7, 18, 19];
        if (sunsetHours.includes(hour)) {
            weatherBg.classList.add('sunset');
        } else if (isNight) {
            weatherBg.classList.add('night');
        } else {
            weatherBg.classList.add('sunny');
            sunRays.classList.add('active');
        }
    }

    // Night mode overlay (stars on top of any background)
    if (isNight && !weatherBg.classList.contains('night')) {
        startStars();
    }
    if (weatherBg.classList.contains('night')) {
        startStars();
    }
}

// Rain Animation
function startRain() {
    rainContainer.classList.add('active');
    rainContainer.innerHTML = '';

    for (let i = 0; i < 100; i++) {
        const drop = document.createElement('div');
        drop.className = 'raindrop';
        drop.style.left = Math.random() * 100 + '%';
        drop.style.top = -(Math.random() * 100) + 'px';
        drop.style.animationDuration = (Math.random() * 0.5 + 0.5) + 's';
        drop.style.animationDelay = Math.random() * 2 + 's';
        rainContainer.appendChild(drop);
    }
}

// Snow Animation
function startSnow() {
    snowContainer.classList.add('active');
    snowContainer.innerHTML = '';

    const snowflakes = ['❄', '❅', '❆'];

    for (let i = 0; i < 50; i++) {
        const flake = document.createElement('div');
        flake.className = 'snowflake';
        flake.textContent = snowflakes[Math.floor(Math.random() * snowflakes.length)];
        flake.style.left = Math.random() * 100 + '%';
        flake.style.animationDuration = (Math.random() * 3 + 2) + 's';
        flake.style.animationDelay = Math.random() * 5 + 's';
        flake.style.fontSize = (Math.random() * 1 + 0.5) + 'em';
        snowContainer.appendChild(flake);
    }
}

// Stars Animation
function startStars() {
    stars.classList.add('active');
    stars.innerHTML = '';

    for (let i = 0; i < 100; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.animationDelay = Math.random() * 3 + 's';
        stars.appendChild(star);
    }
}

// Lightning Animation
let lightningInterval = null;
function startLightning() {
    lightningInterval = setInterval(() => {
        if (Math.random() > 0.7) {
            lightning.classList.add('flash');
            setTimeout(() => {
                lightning.classList.remove('flash');
            }, 200);
        }
    }, 3000);
}

// Stop All Animations
function stopAllAnimations() {
    rainContainer.classList.remove('active');
    rainContainer.innerHTML = '';

    snowContainer.classList.remove('active');
    snowContainer.innerHTML = '';

    cloudsContainer.classList.remove('active');

    sunRays.classList.remove('active');

    stars.classList.remove('active');
    stars.innerHTML = '';

    lightning.classList.remove('flash');

    if (lightningInterval) {
        clearInterval(lightningInterval);
        lightningInterval = null;
    }
}

// Utility Functions
function showLoading() {
    loading.classList.remove('hidden');
    mainWeather.classList.add('hidden');
}

function hideLoading() {
    loading.classList.add('hidden');
}

function showError(message) {
    error.textContent = `⚠️ ${message}`;
    error.classList.remove('hidden');
    setTimeout(() => error.classList.add('hidden'), 5000);
}

function hideError() {
    error.classList.add('hidden');
}

// Load weather on page load
window.addEventListener('load', () => {
    fetchWeather();
});

// Update time every minute
setInterval(() => {
    if (!mainWeather.classList.contains('hidden')) {
        document.getElementById('currentTime').textContent = new Date().toLocaleString('en-US', {
            weekday: 'long',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}, 60000);
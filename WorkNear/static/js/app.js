function useMyLocation(latId, lonId, formId) {
  if (!navigator.geolocation) {
    alert("Geolocation is not supported by this browser. Enter coordinates manually.");
    return;
  }
  navigator.geolocation.getCurrentPosition(
    function (position) {
      document.getElementById(latId).value = position.coords.latitude.toFixed(6);
      document.getElementById(lonId).value = position.coords.longitude.toFixed(6);
      if (formId) document.getElementById(formId).requestSubmit();
      else alert("Location filled in. Check the map pin, then submit the form.");
    },
    function () {
      alert("Could not access your location. Allow location permission or enter coordinates manually.");
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
  );
}

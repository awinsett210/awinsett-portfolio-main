function displayInfo() {
  const dropdown = document.getElementById("infoDropdown");
  const selectedValue = dropdown.value;
  const infoDisplay = document.getElementById("infoDisplay");

  let infoText = "";

  switch (selectedValue) {
    case "option1":
      infoText = "awinsett210@gmail.com";
      break;
    case "option2":
      infoText = "717-860-1508";
      break;
    default:
      infoText = "Please select an option to see its information.";
  }

  infoDisplay.innerHTML = infoText;
}
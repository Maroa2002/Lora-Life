function toggleAdditionalFields() {
  const role = document.getElementById("role").value;
  document.getElementById("farmerFields").style.display =
    role === "farmer" ? "block" : "none";
  document.getElementById("vetFields").style.display =
    role === "vet" ? "block" : "none";
}

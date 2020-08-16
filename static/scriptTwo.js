// this SO question returning solved the problem of addEventListener returning null
// https://stackoverflow.com/a/57302328/12716823




// CONFIRM BUTTONS

//const confirmStaffBtn = document.querySelector(".btn-staff")
//confirmStaffBtn.addEventListener ("click", (e) =>
//{
//const confirmStaffArray = [];
//const confirmStaffCheckboxes = document.querySelectorAll(".confirmStaffCheckbox");
//console.log(confirmStaffCheckboxes)
//confirmStaffCheckboxes.forEach (el => console.log(el))
//
//console.log("a checkbox got clicked")
//
//})

function someFunc(button) {
  var elements = document.querySelectorAll(
    'input[data-value="' + button.dataset.value + '"]'
  );
  console.log(elements);
  const action = button.dataset.attribute;
  let siblingElement;
  elements.forEach((e) => {
    console.log(e);
    if (action !== e.dataset.attribute) {
      e.disabled = true;
      siblingElement = e;
    }
  });

  const data = { staff_id: button.dataset.value, action: action };

  $.ajax({
    type: "POST",
    url: "/approvals",
    contentType: "application/json; charset=utf-8",
    crossDomain: true,
    dataType: "json",
    data: JSON.stringify(data),
  });
  console.log(data);
}

// I don't think two ajax will work in one js file
// tasks submit command

$(document).ready(() => {
  $("#tasks").submit((e) => {
    const url = "/tasks";
    // console.log(url)
    e.preventDefault();

    let formData = new FormData();
    const formInputs = $("#tasks :input");

    formInputs.each((index, input) => {
      let inputName = input.name;
      if (inputName && inputName.trim() !== "") {
        formData[inputName] = input.value;
      }
    });

    $.ajax({
      type: "POST",
      url: url,
      contentType: "application/json; charset=utf-8",
      crossDomain: true,
      dataType: "json",
      data: JSON.stringify(formData),
      success: function (data, status, jqXHR) {
        alert("Sent!");
        window.location.href = "/admin";
      },
      //      error: function(jqXHR, status) {
      //        alert('fail' + status.code);
      //      }
      error: function (jqXHR, textStatus, errorThrown) {
        alert("Fail: " + jqXHR.responseJSON);
      },
    });
    console.log(formData);
  });
});

// Reports tab

// const showReports = document.getElementById("reportsTab");
// showReports.addEventListener("click", () => {
//   console.log("showReports has been clicked");
//   const reports = document.getElementById("reportsTable");

//   if (reports.classList.contains("d-none")) {
//     reports.classList.remove("d-none");
//     showReports.textContent = "Write Tasks";
//   } else {
//     reports.classList.add("d-none");
//     showReports.textContent = "Tasks";
//   }
// });

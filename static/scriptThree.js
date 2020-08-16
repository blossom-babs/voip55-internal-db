const showReports = document.getElementById("reportsTab");
showReports.addEventListener ('click', () =>
{
console.log("showReports has been clicked");
const reports = document.getElementById ("reportsTable")

if (reports.classList.contains ("d-none")){
reports.classList.remove("d-none");
showReports.textContent = "Write Report";
}
else{
reports.classList.add("d-none");
showReports.textContent = "Reports";
}
})

  var editor = new Quill('#editor', {
    modules: { toolbar: '#toolbar' },
    theme: 'snow'
  });

$(document).ready(() =>
{
$("#report"). submit((e) =>
{
const url = "/reports";
// console.log(url)
e.preventDefault();

let formData = new FormData ();
const formInputs = $('#report :input');

 formInputs.each((index, input) => {
      let inputName = input.name;
      if (inputName && inputName.trim() !== "") {
        formData[inputName] = input.value
      }
    })


    $.ajax({
      type: "POST",
      url: url,
      contentType: "application/json; charset=utf-8",
      crossDomain: true,
      dataType: "json",
      data: JSON.stringify(formData),
      success: function(data, status, jqXHR) {
        alert("Sent!");
       window.location.href = "/dashboard";
        },
//      error: function(jqXHR, status) {
//        alert('fail' + status.code);
//      }
        error: function(jqXHR, textStatus, errorThrown) {
   alert("Fail: " + jqXHR.responseJSON);
}
 });
    console.log(formData);

})
})

//    const formDates = $('#report :date');
//    const formMessage = $('#report :textarea')

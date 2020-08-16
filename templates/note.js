                // SUPPLIERS INFORMATION

const addSupplier = document.getElementById("add");
addSupplier.addEventListener("click", () => {

var suppliersTable = document.getElementById("suppliersInfo")

    const suppliersRow = suppliersTable.insertRow();

    const suppliersCell1 = suppliersRow.insertCell(0);
    const suppliersCell2 = suppliersRow.insertCell(1);
    const suppliersCell3 = suppliersRow.insertCell(2);
    const suppliersCell4 = suppliersRow.insertCell(3)

    suppliersCell1.innerHTML = `<input type="text" name="supplierName">`;
    suppliersCell2.innerHTML = `<input type="text" name="supplierAddress">`;
    suppliersCell3.innerHTML = `<input type="text" name="supplierContacts">`
    suppliersCell4.innerHTML = `<input type="text" name="supplierEmail">`;
    }
)

const removeSupplier = document.getElementById("remove");
removeSupplier.addEventListener("click", ()=> {
var suppliersTable = document.getElementById("suppliersInfo")
suppliersTable.deleteRow(-1);
})

// OPENING AND CLOSING OF THE FORM

//const openBox = document.getElementById("openComment")
//openBox.addEventListener("click", ()=>{
//const commentBox = document.getElementById("commentDiv")
//const commentTable = document.getElementById("commentTD")
//console.log(commentBox)
//commentTable.classList.remove("d-none")
//commentBox.classList.remove("d-none")
//
//})
//
//const closeBox = document.getElementById("closeComment")
//closeBox.addEventListener("click", ()=>{
//const commentTable = document.getElementById("commentTD")
//const commentBox = document.getElementById("commentDiv")
//commentBox.classList.add("d-none")
//commentTable.classList.add("d-none")
//})

//const commentBox = document.querySelector(`#${id}`)
//const commentTable = document.querySelector(".commentTD")
//commentTable.classList.remove("d-none")
//commentBox.classList.remove("d-none")

     
 // delete client details
 function deleteFunc(pk) {
     // document.getElementById("warning")
     const warning = document.querySelectorAll(`[data-warningId= '${pk}']`)[0]
     warning.classList.remove("d-none")
     console.log(warning)
     // warning

     const ok = document.querySelectorAll(`[data-clientId= '${pk}']`)[0]
     const doNotDelete = document.querySelectorAll(`[data-doNotDeleteId= '${pk}']`)[0]

     if (ok) {
         ok.addEventListener('click', () => {
             warning.classList.add("d-none")
         })
     }
     if (doNotDelete) {
         doNotDelete.addEventListener('click', () => {
             warning.classList.add("d-none")
         })
     }
     // https://stackoverflow.com/questions/50199135/javascript-addeventlistener-if-else-condition-not-work

 }


 // const data = {
 //     action: action,
 //     value: value
 // }

 // $.ajax({
 // type: "POST",
 // url: "/restoreClient",
 // contentType: "application/json; charset=utf-8",
 // crossDomain: true,
 // dataType: "json",
 // data: JSON.stringify(data),
 // success: function (data, status, jqXHR) {
 // window.location.href = "/trash";
 // }
 // });
 // console.log(data);

 //  console.log(`action: ${action} and value ${value}`)

 // delete suppliers details
 function deleteSup(pk) {
     const warningSup = document.querySelectorAll(`[data-warningSupId= '${pk}']`)[0]
     warningSup.classList.remove("d-none")


     const dataDelete = document.querySelectorAll(`[data-delete= '${pk}']`)[0]
     const stopDelete = document.querySelectorAll(`[data-stopDelete= '${pk}']`)[0]

     if (dataDelete) {
         dataDelete.addEventListener('click', () => {
             warningSup.classList.add("d-none")
         })

     }
     if (stopDelete) {
         stopDelete.addEventListener('click', () => {
             warningSup.classList.add("d-none")
         })
     }
 }

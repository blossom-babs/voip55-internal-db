function openForm(id){
console.log(id)
    document.querySelector(`#${id}`).style.display = "inline-block";
}

function closeForm(id){
    document.querySelector(`#${id}`).style.display = "none";
}

function myCreateFunction(){
    var table = document.querySelector(".tableid");
    console.log(table);
    console.dir(table);
    console.log(table.rows[0]);
    var row = table.insertRow();
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    cell1.innerHTML = "<input type='text' class='form-control' name='name'>";
    cell2.innerHTML = "<input type='text' class='form-control' name='contract'>";
    cell3.innerHTML = "<input type='text' class='form-control' name='payg'>";
}

function myDeleteFunction() {
  document.querySelector(".tableid").deleteRow(-1);
    }

function myCreateFunction2(){
var table = document.querySelector(".tableid2");
const rowLength = `demo_${table.rows.length}`
console.log(rowLength)
var row = table.insertRow();
var cell1 = row.insertCell(0);
var cell2 = row.insertCell(1);
var cell3 = row.insertCell(2);
var cell4 = row.insertCell(3);
var cell5 = row.insertCell(4);
var cell6 = row.insertCell(5);

cell1.innerHTML = "<input type='text' class='form-control' name='option_1'>";
cell2.innerHTML = "<input type='text' class='form-control' name='option_2'>";
cell3.innerHTML = "<input type='text' class='form-control' name='other_options'>";
cell4.innerHTML = `<button onclick=openForm('${rowLength}') type="button" class="btn btn-light"><i class='fa fa-comment butter-color'></i> <em>Description</em></button>`;
cell5.innerHTML = "<input type='file' class='form-control' name='file_upload'>";
cell6.innerHTML = `<div id=${rowLength} class=chat-popup><textarea class=textarea name=description placeholder=Description></textarea><br><button onclick=closeForm('${rowLength}') type=button class='btn btn-sm btn-outline-success'>Done</button></div>`;

}

function myDeleteFunction2(){
document.querySelector(".tableid2").deleteRow(-1);
}

function myCreateFunction3(){
    var table = document.querySelector(".tableid3");
    const rowsLength = `demoDesk_${table.rows.length + 1}`
    console.log (rowsLength)
    var row = table.insertRow();
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);


    cell1.innerHTML = "<input class='form-control' type='date' name='date'>";
    cell2.innerHTML = "<input class='form-control' type='text' name='staff_on_duty'>";
    cell3.innerHTML = `<button onclick=openForm('${rowsLength}') type="button" class="btn btn-light">
    <i class='fa fa-comment butter-color'></i> <em>Description</em></button>`;
    cell4.innerHTML = `<div class=chat-popup id=${rowsLength}><textarea class=textarea name=service_request placeholder=Password reset>
    </textarea><br><button type=button onclick=closeForm('${rowsLength}') class='btn btn-sm btn-outline-success'>Done</button></div>`;

}

function myDeleteFunction3(){
document.querySelector(".tableid3").deleteRow(-1);
}

function myCreateFunction4(){
var table = document.querySelector(".tableid4")
 const rows_length = `demoOffice_${table.rows.length + 1}`
    var row = table.insertRow();
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);

    cell1.innerHTML = `<input class="form-control" type="text" name="device">`;
    cell2.innerHTML = `<input class="form-control" type="text" name="username">`;
    cell3.innerHTML = `<input class="form-control" type="text" name="password">`;
    cell4.innerHTML = `<button onclick="openForm('${rows_length}')" type="button" class="btn btn-light">
    <i class="fa fa-comment butter-color"></i> <em>Configuration</em></button>`;
    cell5.innerHTML = `<div class="chat-popup" id=${rows_length}><textarea class="textarea" name="configuration"
    placeholder="Configuration box"></textarea><br><button onclick="closeForm('${rows_length}')" type="button"
    class="btn btn-sm btn-outline-success">Done</button></div>`;

}

function myDeleteFunction4(){
document.querySelector(".tableid4").deleteRow(-1);
}

// console.log("edit/{{client_id}}")
$(document).ready(() => {
  $("#form").submit((e) => {
    const url = ((e.target.dataset.client) ? `/edit/${e.target.dataset.client}` : '/addclient')
    console.log(url);
    e.preventDefault();

    let formData = new FormData();
    const formInputs = $('#form :input');

    formInputs.each((index, input) => {
      let inputName = input.name;
      if (inputName && inputName.trim() !== "") {
        formData[inputName] = input.value
      }
    })

        serviceProvided = new Array();
        $('#service_provided tr').each(function(){
        let serviceProvidedData = new Object();
        $(this).find("input[type= 'text']").each (function(){
        serviceProvidedData [this.name] = this.value;
        })
        serviceProvided.push(serviceProvidedData)
        })

      let passwordsDocs = new Array();
      $('#passwords tr').each(function(){
          let passwordsDocsData = new Object();
            $(this).find("td input:text").each(function(){
            passwordsDocsData[this.name] = this.value;

      })
      $(this).find("textarea").each(function(){
      passwordsDocsData[this.name] = this.value;
          })

          $(this).find("input[type = 'file']").each(function(){

            passwordsDocsData[this.name] = this.value;
          })

         passwordsDocs.push(passwordsDocsData)

      })


      let helpdeskService = new Array();
      $('#helpdesk_service tr').each(function(){
        let helpdeskServiceData = new Object();
            $(this).find("input[type='date']").each(function(){
                if (this.name === ""){
                return
                }
                helpdeskServiceData[this.name] = this.value;
                console.log[this.name]
        })
            $(this).find("td input:text").each(function(){
                    helpdeskServiceData[this.name] = this.value;
        })
            $(this).find("textarea"). each(function(){
                helpdeskServiceData[this.name] = this.value;
      })
            helpdeskService.push(helpdeskServiceData)

      })

    let officeDevices = new Array();
      $('#office_devices tr').each(function(){
        let officeDevicesData = new Object();
            $(this).find("input[type='text']").each(function(){
                officeDevicesData[this.name] = this.value;
        })
            $(this).find("textarea"). each(function(){
                officeDevicesData[this.name] = this.value;
      })
            officeDevices.push(officeDevicesData)

      })

    formData["service_provided"] = serviceProvided
    formData["passwords"] = passwordsDocs
    formData["helpdesk_service"] = helpdeskService
    formData["office_devices"] = officeDevices

    console.log(formData)
    $.ajax({
      type: "POST",
      url: url,
      contentType: "application/json; charset=utf-8",
      crossDomain: true,
      dataType: "json",
      data: JSON.stringify(formData),
      success: function(data, status, jqXHR) {
        alert("Saved!");
        if (url === "/addclient"){
    window.location.href = "/addclient";
   }
    else{
   window.location.href = `/client/${e.target.dataset.client}`;
   }

      },
      error: function(jqXHR, status) {
        alert('fail' + status.code);
      }

    });

    console.log(formData);

  })

})



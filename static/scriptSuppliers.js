console.log("this ought to work")

function openComment(id) {
    console.log(id)
    document.querySelector(`#${id}`).style.display = "inline-block";

}

function closeComment(id) {
    document.querySelector(`#${id}`).style.display = "none";

}


// SUPPLY INFORMATION

function suppliersAdd() {
    var tables = document.getElementById("supplyInfo");
    const rowLength = `comment_${tables.rows.length + 1}`
    const rows = tables.insertRow();
    const cell1 = rows.insertCell(0);
    const cell2 = rows.insertCell(1);
    const cell3 = rows.insertCell(2);
    const cell4 = rows.insertCell(3);
    const cell5 = rows.insertCell(4);
    const cell6 = rows.insertCell(5);
    const cell7 = rows.insertCell(6);


    cell1.innerHTML = `<input class="form-control" type="text" placeholder="Service" name="typeOfService">`;
    cell2.innerHTML = `<input class="form-control" type="text" placeholder="Reference" name="paymentRef">`;
    cell3.innerHTML = `<input class="form-control" type="text" placeholder="Amount" name="paymentAmt">`;
    cell4.innerHTML = `<input class="form-control" type="text" placeholder="Customer" name="customer">`;
    cell5.innerHTML = `<input class="form-control" type="text" placeholder="Expiry" name="expiryDate">`;
    cell6.innerHTML = `<button onclick="openComment('${rowLength}')" type="button" class="btn btn-light">
                     <i class="fa fa-comment butter-color"></i><em>Comment</em></button>`;
    cell7.innerHTML = `<div class="chat-popup commentDiv " id="${rowLength}"><textarea class="textarea" name="comment"></textarea>
                     <button onclick="closeComment('${rowLength}')" type="button" class="btn btn-sm btn-outline-success">Done</button>
                     </div>`;
}


function suppliersRemove() {
    var tables = document.getElementById("supplyInfo")
    tables.deleteRow(-1);
}


$(document).ready(() => {
    $("#suppliers").submit((e) => {
        //const url ="/suppliers"

        const url = ((e.target.dataset.supplier) ? `/editsupplier/${e.target.dataset.supplier}` : '/suppliers')
        console.log(url)
        e.preventDefault()

        let formData = new FormData();

        const formInputs = $('#form-group :input');
        console.log(formInputs)

        formInputs.each((index, input) => {
            let inputName = input.name;
            if (inputName && inputName.trim() !== "") {
                formData[inputName] = input.value
            }
        })

        let supplyInfo = new Array();
        $('#supplyInfo tr').each(function () {
            let supplyInfoData = new Object();
            $(this).find("input[type='text']").each(function () {
                supplyInfoData[this.name] = this.value;
            })
            $(this).find("textarea").each(function () {
                supplyInfoData[this.name] = this.value;
            })
            supplyInfo.push(supplyInfoData)
        })

        formData["supply_info"] = supplyInfo
        console.log(formData)

        $.ajax({
            type: "POST",
            url: url,
            contentType: "application/json; charset=utf-8",
            crossDomain: true,
            dataType: "json",
            data: JSON.stringify(formData),
            success: function (data, status, jqXHR) {
                alert("Saved!");
                if (url === "/suppliers"){
                   window.location.href = "/suppliers";
                   } 
                else{
                 window.location.href = `/existingsupplier/${e.target.dataset.supplier}` ;
                   }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert("Fail: " + jqXHR.responseJSON);
            }

        });



        // the ready and submit function closing boxes
    })
})
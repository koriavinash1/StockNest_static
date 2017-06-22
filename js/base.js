background = ['rgba(255, 99, 132, 0.2)','rgba(54, 162, 235, 0.2)','rgba(255, 206, 86, 0.2)','rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)', 'rgba(255, 200, 200, 0.2)', 'rgba(75, 200, 192, 0.2)','rgba(255, 102, 255,0.2','rgba(255, 170, 64, 0.2'];

VEDL_CLOSING_PRICE_DATA.shift(); VEDL_CLOSING_PRICE_LABEL.shift();
BPCL_CLOSING_PRICE_DATA.shift(); BPCL_CLOSING_PRICE_LABEL.shift();
HINDALCO_CLOSING_PRICE_DATA.shift(); HINDALCO_CLOSING_PRICE_LABEL.shift();
RELIANCE_CLOSING_PRICE_DATA.shift(); RELIANCE_CLOSING_PRICE_LABEL.shift();
YESBANK_CLOSING_PRICE_DATA.shift(); YESBANK_CLOSING_PRICE_LABEL.shift();

function drawGraph(type,id,data,background,labels,company){
  $("#canvas_"+id.toString()).remove();
  $("#parent_"+id.toString()).append($('<canvas />', {'id':'canvas_'+id.toString()}).height(550).width(850));
  var qid = document.getElementById("canvas_"+id.toString());
  var myChart = new Chart(qid, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: company+'_prediction',
        data: data,
        backgroundColor:'rgba(255, 99, 132, 0.2)',
        borderWidth: 2,
      }]
    },
    options: {
        responsive: false,
    }
  });
}

function multipleGraph(type,id,data1,data2,background,labels1, companyname1, companyname2){
  $("#canvas_"+id.toString()).remove();
  $("#parent_"+id.toString()).append($('<canvas />', {'id':'canvas_'+id.toString()}).height(550).width(850));
  var qid = document.getElementById("canvas_"+id.toString());
  var myChart = new Chart(qid, {
    type: 'line',
    data: {
      labels: labels1,
      datasets: [{
        label: companyname1 + '_prediction',
        data: data2,
        backgroundColor:'rgba(54, 162, 235, 0.2)',
        borderWidth: 2,
      },
      {
        label: companyname2 + "_prediction",
        data: data1,
        backgroundColor:'rgba(255, 159, 64, 0.2)',
        borderWidth: 2,
      }]
    },
    options: {
        responsive: false,
    }
  });
}

$('#high1').hide();$('#high2').hide();$('#low1').hide();$('#low2').hide();$('#mid1').hide();$('#mid2').hide();
$('#labelcomp1').hide();$('#labelcomp2').hide();$('#comparebtn').hide();$('#errtbid').hide();
$("#risktype").change(function()
{ 
  $('#labelcomp1').show();$('#labelcomp2').show();$('#comparebtn').show();$('#errtbid').show(); 
     risk_type = $(this).val();
     if(risk_type == 'HIGH'){ $('#high1').show();$('#high2').show();$('#low1').hide();$('#low2').hide();$('#mid1').hide();$('#mid2').hide();}
     else if(risk_type == 'MID'){$('#high1').hide();$('#high2').hide();$('#low1').hide();$('#low2').hide();$('#mid1').show();$('#mid2').show();}
     else if(risk_type == 'LOW'){$('#high1').hide();$('#high2').hide();$('#low1').show();$('#low2').show();$('#mid1').hide();$('#mid2').hide();} 
});


$('#errormodel').html(
  '<tr><td>VEDL</td><td>'+VEDL_MAPE+
  '</td><td>'+VEDL_RMSE+'</td></tr><tr><td>BPCL</td><td>'+BPCL_MAPE+'</td><td>'+BPCL_RMSE+'</td></tr><tr><td>RELIANCE</td><td>'+RELIANCE_MAPE+'</td><td>'+RELIANCE_RMSE+'</td></tr><tr><td>HINDALCO</td><td>'+HINDALCO_MAPE+'</td><td>'+HINDALCO_RMSE+'</td></tr><tr><td>YESBANK</td><td>'+YESBANK_MAPE+'</td><td>'+YESBANK_RMSE+'</td></tr>');


$('#stockbtn').click(function(){
  var companyname = $('#stockCompany').val();
  var predictionlen = $('#stockPrediction').val();
  if(companyname == "VEDL"){ data = VEDL_CLOSING_PRICE_DATA;  labels = VEDL_CLOSING_PRICE_LABEL;}
  else if(companyname == "BPCL"){ data = BPCL_CLOSING_PRICE_DATA;  labels = BPCL_CLOSING_PRICE_LABEL;}
  else if(companyname == "HINDALCO"){ data = HINDALCO_CLOSING_PRICE_DATA;  labels = HINDALCO_CLOSING_PRICE_LABEL;}
  else if(companyname == "RELIANCE"){ data = RELIANCE_CLOSING_PRICE_DATA;  labels = RELIANCE_CLOSING_PRICE_LABEL;}
  else if(companyname == "YESBANK"){ data = YESBANK_CLOSING_PRICE_DATA;  labels = YESBANK_CLOSING_PRICE_LABEL;}
  else{ alert("Select company...");return;}

  if(predictionlen != 2){alert("Currently only prediction length = 2, is allowed..");return;}
  drawGraph("lines", "stockprediction", data, background, labels, companyname)
});

$('#comparebtn').click(function(){
  if(risk_type == 'HIGH'){
    var companyname1 = $("#high1").val();
    var companyname2 = $("#high2").val();
  }
  else if(risk_type == 'MID'){
    var companyname1 = $("#mid1").val();
    var companyname2 = $("#mid2").val();
  }
  else if(risk_type == 'LOW'){
    var companyname1 = $("#low1").val();
    var companyname2 = $("#low2").val();
  }

  if(companyname1 === companyname2) {alert("Both companies can't be same...");return;};

  if(companyname1 == "VEDL"){ data1 = VEDL_CLOSING_PRICE_DATA;  labels1 = VEDL_CLOSING_PRICE_LABEL;}
  else if(companyname1 == "BPCL"){ data1 = BPCL_CLOSING_PRICE_DATA;  labels1 = BPCL_CLOSING_PRICE_LABEL;}
  else if(companyname1 == "HINDALCO"){ data1 = HINDALCO_CLOSING_PRICE_DATA;  labels1 = HINDALCO_CLOSING_PRICE_LABEL;}
  else if(companyname1 == "RELIANCE"){ data1 = RELIANCE_CLOSING_PRICE_DATA;  labels1 = RELIANCE_CLOSING_PRICE_LABEL;}
  else if(companyname1 == "YESBANK"){ data1 = YESBANK_CLOSING_PRICE_DATA;  labels1 = YESBANK_CLOSING_PRICE_LABEL;}
  else{ alert("Select company1...");return;}

  if(companyname2 == "VEDL"){ data2 = VEDL_CLOSING_PRICE_DATA;  labels2 = VEDL_CLOSING_PRICE_LABEL;}
  else if(companyname2 == "BPCL"){ data2 = BPCL_CLOSING_PRICE_DATA;  labels2 = BPCL_CLOSING_PRICE_LABEL;}
  else if(companyname2 == "HINDALCO"){ data2 = HINDALCO_CLOSING_PRICE_DATA;  labels2 = HINDALCO_CLOSING_PRICE_LABEL;}
  else if(companyname2 == "RELIANCE"){ data2 = RELIANCE_CLOSING_PRICE_DATA;  labels2 = RELIANCE_CLOSING_PRICE_LABEL;}
  else if(companyname2 == "YESBANK"){ data2 = YESBANK_CLOSING_PRICE_DATA;  labels2 = YESBANK_CLOSING_PRICE_LABEL;}
  else{ alert("Select company2...");return;}

  multipleGraph('lines','stockcompare',data1,data2,background,labels1, companyname1, companyname2)
});
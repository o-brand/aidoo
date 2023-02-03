//Points
var points = 5;
var days = 0;
var hours = 1;

// Recalculate points
$("select[name='duration_days']").on("input", function(e) {
  value = Number.parseFloat(e.target.value);

  //If the new value is a normal number
  if (!Number.isNaN(value)) {
    points += (value - days) * 24 * 5;
    days = value;

    //Display the new points
    $("#points").html(points);
  }
});
$("select[name='duration_hours']").on("input", function(e) {
  value = Number.parseFloat(e.target.value);

  //If the new value is a normal number
  if (!Number.isNaN(value)) {
    points += (value - hours) * 5;
    hours = value;

    //Display the new points
    $("#points").html(points);
  }
});

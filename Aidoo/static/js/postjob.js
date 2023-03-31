//Points
var points = 12;
var hhours = 0;
var hours = 1;

// Recalculate points
$("select[name='duration_hours']").on("input", function(e) {
  value = Number.parseFloat(e.target.value);

  //If the new value is a normal number
  if (!Number.isNaN(value)) {
    points += (value - hours) * 12;
    hours = value;

    if (points > 18)
      hourstxt = "hours"
    else
      hourstxt = "hour"

    //Display the new points
    $("#hourstxt").html(hourstxt)
    $("#points").html(points);
  }
});
$("select[name='duration_half_hours']").on("input", function(e) {
  value = Number.parseFloat(e.target.value);

  //If the new value is a normal number
  if (!Number.isNaN(value)) {
    points += (value - hhours) / 60 * 12;
    hhours = value;

    if (points > 18)
      hourstxt = "hours"
    else
      hourstxt = "hour"

    //Display the new points
    $("#hourstxt").html(hourstxt)
    $("#points").html(points);
  }
});

$("select[name='duration_hours']").trigger('input');
$("select[name='duration_half_hours']").trigger('input');

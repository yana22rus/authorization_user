function check()
{


  let checkbox = document.getElementById("check_box");
  let seo_title = document.getElementById("seo_title")
  let seo_description = document.getElementById("seo_description")
  if (checkbox.checked == true)
  {
      seo_title.hidden = false;
    seo_description.hidden = false;

  }else{
        seo_title.hidden = true;
    seo_description.hidden = true;

  }
}
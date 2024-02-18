document.addEventListener("DOMContentLoaded", () => {
  let side_bar = document.querySelector(".side-bar");
  let toggle = document.querySelector(".toggle-seller");
  toggle?.addEventListener("click", () => {
    if (side_bar?.style.left == "10px") {
      side_bar.style.left = "-320px";
      toggle.style.transform = "rotate(0deg)";
      toggle.innerHTML = '<i class="fa-solid fa-bars-staggered fa-2x"></i>';
    } else {
      side_bar.style.left = "10px";
      toggle.style.transform = "rotate(360deg)";
      toggle.innerHTML = '<i class="fa-solid fa-x fa-2x"></i>';
    }
  });
  const coupon_code = document.querySelectorAll(".coupon-code");
  for (let i = 0; i < coupon_code.length; i++) {
    coupon_code[i].addEventListener("click", () => {
      navigator.clipboard.writeText(coupon_code[i].innerHTML);
      let message = coupon_code[i].parentElement.querySelector(".copy-message");
      let input = coupon_code[i].parentElement?.parentElement?.querySelector("form")?.querySelector('input[name="code"]')
      input.value = coupon_code[i].innerHTML
      message.innerHTML = `${coupon_code[i].innerHTML} copied!`;
      message.style.background = "rgb(0, 255, 100)";
      message.style.boxShadow = "0 0 5px black";
      setTimeout(() => {
        message.innerHTML = "";
        message.style.background = "inherit";
        message.style.boxShadow = "0 0 0 white";
      }, 1000);
    });
  }
});

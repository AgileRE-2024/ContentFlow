const accordionBtns = document.querySelectorAll(".accordion__title");

accordionBtns.forEach((button) => {
  button.addEventListener("click", (event) => {
    let accCollapse = button.nextElementSibling;

    if (!button.classList.contains("collapsing")) {
      // open accordion item
      if (!button.classList.contains("open")) {
        accCollapse.style.display = "block";
        let accHeight = accCollapse.clientHeight;

        setTimeout(() => {
          accCollapse.style.height = accHeight + "px";
          accCollapse.style.display = "";
        }, 1);

        accCollapse.classList = "accordion__collapse collapsing";

        setTimeout(() => {
          accCollapse.classList = "accordion__collapse collapse open";
        }, 300);
      }
      //close accordion item
      else {
        accCollapse.classList = "accordion__collapse collapsing";

        setTimeout(() => {
          accCollapse.style.height = "0px";
        }, 1);

        setTimeout(() => {
          accCollapse.classList = "accordion__collapse collapse";
          accCollapse.style.height = "";
        }, 300);
      }

      button.classList.toggle("open");
    }
  });
});

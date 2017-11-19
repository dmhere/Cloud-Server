        var modal_hdfs = document.getElementById('hdfs');        
        var modal_mr = document.getElementById("mr")
        var img_mr = document.getElementById('mrimg');
        var img_hdfs = document.getElementById('hdfsimg');
        img_mr.onclick = function(){
                modal_mr.style.display = "block";
            }
        img_hdfs.onclick = function(){
                modal_hdfs.style.display = "block";
            }
            // Get the <span> element that closes the modal
        var span = document.getElementsByClassName("close")[0];

            // When the user clicks on <span> (x), close the modal
        span.onclick = function() { 
                if (event.target == modal_hdfs) {
                    modal_hdfs.style.display = "none";
                }
                if (event.target == modal_mr) {
                    modal_mr.style.display = "none";
                }
            }
        window.onclick = function(event) {
                if (event.target == modal_hdfs) {
                    modal_hdfs.style.display = "none";
                }
                if (event.target == modal_mr) {
                    modal_mr.style.display = "none";
                }
            }
    
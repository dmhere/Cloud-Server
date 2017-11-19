function displayInput(clicked_id)  {
                 var p =  clicked_id;
                 if (p == 'hdfs_man_radio')
                    {
                        var x = document.getElementById('hdfs_manual_radio');
                        x.style.display='block';
                        var inputCount = document.getElementById('hdfs_manual_radio').getElementsByTagName('input').length;
                        if (inputCount<=0) {
                            var x = document.createElement("INPUT");
                            x.setAttribute("type", "text");
                            x.setAttribute("name", "namenodeIp");
                            x.setAttribute("placeholder", "Enter ip of namenodenode");
                            document.getElementById("hdfs_manual_radio").innerHTML += "Enter the ip of namenode";
                            document.getElementById("hdfs_manual_radio").appendChild(x);

                            var x = document.createElement("INPUT");
                            x.setAttribute("type", "password");
                            x.setAttribute("name", "namenodePass");
                            x.setAttribute("placeholder", "password of namenode");
                            document.getElementById("hdfs_manual_radio").innerHTML += "Enter the password";
                            document.getElementById("hdfs_manual_radio").appendChild(x);
                            document.getElementById("hdfs_manual_radio").innerHTML += " <br /> <br />";
                        }
                            inputCount = document.getElementById('hdfs_manual_radio').getElementsByTagName('input').length;
                            var count = document.getElementById("noofdn").value;
                            for (i=1; i <= count-(inputCount/2)+1; i++) {
                            var x = document.createElement("INPUT");
                            x.setAttribute("type", "text");
                            x.setAttribute("name", "dnIp"+i);
                            x.setAttribute("placeholder", "Enter ip of datanode");
                            document.getElementById("hdfs_manual_radio").innerHTML += "Enter the ip of datanode";
                            document.getElementById("hdfs_manual_radio").appendChild(x);

                            var x = document.createElement("INPUT");
                            x.setAttribute("type", "password");
                            x.setAttribute("name", "dnPass"+i);
                            x.setAttribute("placeholder", "password of this ip");
                            document.getElementById("hdfs_manual_radio").innerHTML += "Enter the password";
                            document.getElementById("hdfs_manual_radio").appendChild(x);
                            document.getElementById("hdfs_manual_radio").innerHTML += " <br />";

                        }
                    }

                if (p == 'mr_man_radio')
                    {
                        var x = document.getElementById('mr_manual_radio');
                        x.style.display='block';
                        var inputCount = document.getElementById('mr_manual_radio').getElementsByTagName('input').length;
                        if (inputCount<=0) {
                            var x = document.createElement("INPUT");
                            x.setAttribute("type", "text");
                            x.setAttribute("name", "namenodeIp");
                            x.setAttribute("placeholder", "Enter ip of Jobtracker");
                            document.getElementById("mr_manual_radio").innerHTML += "Enter the ip of Jobtracker";
                            document.getElementById("mr_manual_radio").appendChild(x);

                            var x = document.createElement("INPUT");
                            x.setAttribute("type", "password");
                            x.setAttribute("name", "namenodePass");
                            x.setAttribute("placeholder", "password of jobtracker");
                            document.getElementById("mr_manual_radio").innerHTML += "Enter the password";
                            document.getElementById("mr_manual_radio").appendChild(x);
                            document.getElementById("mr_manual_radio").innerHTML += " <br /> <br />";
                        }
                            inputCount = document.getElementById('mr_manual_radio').getElementsByTagName('input').length;
                            var count = document.getElementById("nooftt").value;
                            for (i=1; i <=count-(inputCount/2)+1; i++) {
                            var x = document.createElement("INPUT");
                            x.setAttribute("type", "text");
                            x.setAttribute("name", "dnIp"+i);
                            x.setAttribute("placeholder", "Enter ip of tasktracker");
                            document.getElementById("mr_manual_radio").innerHTML += "Enter the ip of tasktracker";
                            document.getElementById("mr_manual_radio").appendChild(x);

                            var x = document.createElement("INPUT");
                            x.setAttribute("type", "password");
                            x.setAttribute("name", "dnPass"+i);
                            x.setAttribute("placeholder", "password of this ip");
                            document.getElementById("mr_manual_radio").innerHTML += "Enter the password";
                            document.getElementById("mr_manual_radio").appendChild(x);
                            document.getElementById("mr_manual_radio").innerHTML += " <br />";

                        }
                    }
                            /*if inputCount > count then you need to remove some of input box*/
}

function hideInput(clicked_id) {
                    var p =  clicked_id;
                    if (p == 'hdfs_od_radio') {
                        var x= document.getElementById('hdfs_manual_radio');
                        x.style.display = 'none';
                    }
                    if (p == 'mr_od_radio') {
                        var x= document.getElementById('mr_manual_radio');
                        x.style.display = 'none';
                    }
}


function showform(clicked_id) {
	var p =  clicked_id;
	if (p == 'hdfs_link')
                    {
                        var a = document.getElementById('hdfs_form_div');
                        a.style.display='block';
                        var b = document.getElementById('mr_form_div');
                        b.style.display='none';
                        var c = document.getElementById('stass_form_div');
                        c.style.display='none';
                        var d = document.getElementById('iaas_form_div');
                        d.style.display='none';
                        var e = document.getElementById('caas_form_div');
                        e.style.display='none';
                        var f = document.getElementById('saas_form_div');
                        f.style.display='none';		
}
    if (p == 'mr_link')
                    {
                        var a = document.getElementById('hdfs_form_div');
                        a.style.display='none';
                        var b = document.getElementById('mr_form_div');
                        b.style.display='block';
                        var c = document.getElementById('stass_form_div');
                        c.style.display='none';
                        var d = document.getElementById('iaas_form_div');
                        d.style.display='none';
                        var e = document.getElementById('caas_form_div');
                        e.style.display='none';
                        var f = document.getElementById('saas_form_div');
                        f.style.display='none';		
}
    if (p == 'stass_link')
                    {
                        var a = document.getElementById('hdfs_form_div');
                        a.style.display='none';
                        var b = document.getElementById('mr_form_div');
                        b.style.display='none';
                        var c = document.getElementById('stass_form_div');
                        c.style.display='block';
                        var d = document.getElementById('iaas_form_div');
                        d.style.display='none';
                        var e = document.getElementById('caas_form_div');
                        e.style.display='none';
                        var f = document.getElementById('saas_form_div');
                        f.style.display='none';		
}
    if (p == 'iaas_link')
                    {
                        var a = document.getElementById('hdfs_form_div');
                        a.style.display='none';
                        var b = document.getElementById('mr_form_div');
                        b.style.display='none';
                        var c = document.getElementById('stass_form_div');
                        c.style.display='none';
                        var d = document.getElementById('iaas_form_div');
                        d.style.display='block';
                        var e = document.getElementById('caas_form_div');
                        e.style.display='none';
                        var f = document.getElementById('saas_form_div');
                        f.style.display='none';		
}
    if (p == 'caas_link')
                    {
                        var a = document.getElementById('hdfs_form_div');
                        a.style.display='none';
                        var b = document.getElementById('mr_form_div');
                        b.style.display='none';
                        var c = document.getElementById('stass_form_div');
                        c.style.display='none';
                        var d = document.getElementById('iaas_form_div');
                        d.style.display='none';
                        var e = document.getElementById('caas_form_div');
                        e.style.display='block';
                        var f = document.getElementById('saas_form_div');
                        f.style.display='none';		
}
    if (p == 'saas_link')
                    {
                        var a = document.getElementById('hdfs_form_div');
                        a.style.display='none';
                        var b = document.getElementById('mr_form_div');
                        b.style.display='none';
                        var c = document.getElementById('stass_form_div');
                        c.style.display='none';
                        var d = document.getElementById('iaas_form_div');
                        d.style.display='none';
                        var e = document.getElementById('caas_form_div');
                        e.style.display='none';
                        var f = document.getElementById('saas_form_div');
                        f.style.display='block';		
}
}


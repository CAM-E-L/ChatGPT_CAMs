/* add button: */
const saveButton = `<button id="saveCAM" onclick="saveCam()" class="material-icons" title="Save CAM on server" style="margin-right: 5px;">save</button>`;
var target = document.getElementById("rightButton");
target.innerHTML += saveButton;

// language file
$(function () {
    document.getElementById("saveCAM").title = languageFileOut.btr_02; // buttons top right (btr)

    document.getElementById("dialogConfirmSave").title = languageFileOut.confirmSaving_01_title; // title confirm saving

});


function updateQueryStringParameter(uri, key, value) {
    var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
    var separator = uri.indexOf("?") !== -1 ? "&" : "?";

    if (uri.match(re)) {
        return uri.replace(re, "$1" + key + "=" + value + "$2");
    } else {
        return uri + separator + key + "=" + value;
    }
}

function saveCam() {
    var CAMnodes = CAM.nodes.filter((element) => element.isActive === true);
    var CAMconnectors = CAM.connectors.filter(
        (element) => element.isActive === true
    );

    // every concept should include text
    var CAMnodesNoText = CAMnodes.filter(
        (element) => element.text.length === 0
    );
    console.log(CAMnodesNoText);
    if (CAMnodesNoText.length > 0) {
        toastr.warning(
            languageFileOut.popSave_01emptyNodes,
            CAMnodesNoText.length + languageFileOut.popSave_02emptyNodes,
            {
                closeButton: true,
                timeOut: 2000,
                positionClass: "toast-top-center",
                preventDuplicates: true,
            }
        );
        return false;
    }

    // every concept should include at least 3 characters
    var CAMnodesFewText = CAMnodes.filter(
        (element) => element.text.length < 3
    );

    if (CAMnodesFewText.length > 0) {
        toastr.warning(
            languageFileOut.popSave_01insufficientCharsNodes,
            CAMnodesFewText.length + languageFileOut.popSave_02insufficientCharsNodes,
            {
                closeButton: true,
                timeOut: 2000,
                positionClass: "toast-top-center",
                preventDuplicates: true,
            }
        );
        return false;
    }

    // necessary # of concepts
    if (CAMnodes.length < config.ConNumNodes) {
        toastr.warning(
            languageFileOut.popSave_01numNodes,
            languageFileOut.popSave_02numNodes +
            config.ConNumNodes +
            languageFileOut.popSave_03numNodes,
            {
                closeButton: true,
                timeOut: 2000,
                positionClass: "toast-top-center",
                preventDuplicates: true,
            }
        );
        return false;
    } else if (CAMnodes.length - 1 > CAMconnectors.length) {
        // CAMnodes.every(element => element.isConnected !== true)
        /* 
        test:
        necessary condition -> everything is connected using simple checks (still possible that there are X non-connected components) 
        */
        console.log("CAMconnectors.length: ", CAMconnectors.length);
        console.log("CAM.nodes.length: ", CAMnodes.length);

        // console.log(CAMnodes.every(element => element.isConnected !== true));
        toastr.warning(
            languageFileOut.popSave_01unconnectedA,
            languageFileOut.popSave_02unconnectedA,
            {
                closeButton: true,
                timeOut: 2000,
                positionClass: "toast-top-center",
                preventDuplicates: true,
            }
        );

        return false;
    } else {
        addElementsCy();
        var ResbfsAl = bfsAlgorithm("#" + cy.nodes()[0].id());
        console.log("num of distinct components of CAM: ", ResbfsAl);

        if (ResbfsAl !== 1) {
            toastr.warning(
                languageFileOut.popSave_01unconnectedB,
                languageFileOut.popSave_02unconnectedB +
                " " +
                ResbfsAl +
                languageFileOut.popSave_03unconnectedB,
                {
                    closeButton: true,
                    timeOut: 2000,
                    positionClass: "toast-top-center",
                    preventDuplicates: true,
                }
            );

            return false;
        } else {
            // confirm saving
            $("#dialogConfirmSave").dialog("open");
        }
    }
}

function saveCAMsuccess() {
    toastr.success(languageFileOut.popSave_01savedData, {
        closeButton: true,
        timeOut: 4000,
        positionClass: "toast-top-center",
        preventDuplicates: true,
    });

    // after 4 seconds
    var delay = (function () {
        var timer = 0;
        return function (callback, ms) {
            clearTimeout(timer);
            timer = setTimeout(callback, ms);
        };
    })();

    delay(function () {
        // set defocus data
        if (config.fullScreen == true) {
            CAM.defocusCAM = arraydefocusevent;
        }

        /* if server is >>> JATOS <<< */
        console.log("usingJATOS: ", usingJATOS);
        if (usingJATOS) {
            if (typeof jatos.jQuery === "function") {
                // if an ID was sent via URL param overwrite CAM creator
                if (
                    Object.keys(jatos.urlQueryParameters).indexOf(
                        "participantID"
                    ) >= 0
                ) {
                    CAM.creator = jatos.urlQueryParameters.participantID;
                } else {
                    CAM.creator = "noID";
                }

                // If JATOS is available, send data there
                var resultJson = CAM;
                console.log(
                    "my result data sent to JATOS first and final time"
                );
                jatos
                    .submitResultData(resultJson)
                    .then(() => console.log("success"))
                    .catch(() => console.log("error"));

                // > with adaptive design
                if (config.AdaptiveStudy) {
                    var newUrl = updateQueryStringParameter(
                        config.ADAPTIVESTUDYurl,
                        "participantID",
                        CAM.creator
                    );
                    jatos.endStudyAndRedirect(
                        newUrl,
                        true,
                        "everything worked fine"
                    );
                } else {
                    jatos.endStudy(true, "everything worked fine");
                }
            }
        }

        /* if server is >>> MangoDB <<< */
        console.log("usingMangoDB: ", usingMangoDB);
        if (usingMangoDB) {

            // URL of the API endpoint

            async function getData() {
                const url = 'http://localhost:3000/api/try';
          
                const get = await fetch(url)
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error('Error:', error));
            }

            getData();


            async function getData2() {
                const url = 'http://localhost:3000/api/try';
                const headers = {'Content-Type':'application/json'}

                console.log("getData2")
                const get = await fetch(url, {
                    method: 'GET',   // Specifying the HTTP method
                    headers: headers  // Including headers in the request
                })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error('Error:', error));
            }
           // getData2();



           async function postData() {
            const url = 'http://localhost:3000/api/try';
            const headers = {'Content-Type':'application/json'}

            console.log("postData")
            const post = await fetch(url, {
                method: 'POST',   // Specifying the HTTP method
                headers: headers,  // Including headers in the request
                body: JSON.stringify({
                    name: 'France',
                    cam: CAM,
                    welcomeYourGirl: 'Hello Sarah'
                }),
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
        }
        postData()

            /*
            // URL of the API endpoint
            const url = 'https://qxeipkcoazhuwnelucih.supabase.co/rest/v1/countries';

            // Data to be sent in the POST request
            const data = {
                id: '99',
                name: 'France'
            };

            // Headers can include things like API keys or content type
            const headers = {
                'Content-Type': 'application/json',
                'apikey': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF4ZWlwa2NvYXpodXduZWx1Y2loIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTY4OTQ1MDMsImV4cCI6MjAzMjQ3MDUwM30.DJPV5UY_zVnjFVvN9H3NnXNAl7GcuTQYwNanrHb-PYI',
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF4ZWlwa2NvYXpodXduZWx1Y2loIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTY4OTQ1MDMsImV4cCI6MjAzMjQ3MDUwM30.DJPV5UY_zVnjFVvN9H3NnXNAl7GcuTQYwNanrHb-PYI'
            };

            console.log("data", data)

            // Using fetch to send a POST request
            fetch(url, {
                method: 'POST',   // Specifying the HTTP method
                body: JSON.stringify(data),  // Converting data into JSON string
                headers: headers  // Including headers in the request
            })
                .then(response => {
                    if (response.ok) {
                        return response.json();  // Parsing the JSON response body
                    } else {
                        throw new Error('Failed to fetch: ' + response.status);
                    }
                })
                .then(data => {
                    console.log('Success:', data);  // Handling the JSON data response
                })
                .catch(error => {
                    console.error('Error:', error);  // Handling errors
                });

*/





            /*



            async function pushData() {
                let info = {
                    method: "POST",
                    body: JSON.stringify({
                        jwt: token,
                        cam: CAM,
                    }),
                    headers: {
                        'Accept': "application/json",
                        'Content-Type': "application/json",
                    },
                };

                console.log("info", info)

                const res = await fetch(
                    webAddress + "participants/submitExperiment",
                    info
                );



                if (res.status == 201) {
                    window.location =
                        linkRedirect +
                        "?participantID=" +
                        CAM.creator;

                    /*
                    "?jwt=" +
                    token +
                
                }
            }
            pushData();
                */
        }

        /* if NO server >>> <<< */
        if (!usingJATOS && !usingMangoDB) {
            toastr.success(languageFileOut.popSave_01notSavedData, {
                closeButton: true,
                timeOut: 4000,
                positionClass: "toast-top-center",
                preventDuplicates: true,
            });
        }
    }, 4000); // end delay
}

import React, { useState, useEffect } from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";

function App() {
  let [formData, setFormData] = useState({
    hall: "",
    startDate: "",
    endDate: "",
    doubleDuty: false,
    raDuty: true,
  });

  let [staffData, setStaffData] = useState([
    {
      name: "",
      preferences: [""],
      SRA: false,
    },
  ]);

  let [isLoading, setLoading] = useState(false);

  const sendFormData = async (formEvent) => {
    formEvent.preventDefault();
    setLoading(true)

    formData.staffData = staffData;
    const requestOptions = {
      method: "POST",
      "Content-Type": "application/json",
      body: JSON.stringify(formData),
      responseType:
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    };

    let response = await fetch(
      window.location.href + "schedule_duty",
      requestOptions
    );

    //Download Excel File from website
    const link = document.createElement("a");
    const url = URL.createObjectURL(await response.blob());

    link.download = formData.hall.concat(" ", "Duty Calendar");
    link.href = url;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    setLoading(false)
  };

  //For Some reason I have to use funcs to increase the size of my states
  //If I directly call the functions React crashes with error too many re renders
  function addStaffMember() {
    let data = { name: "", preferences: [""] };
    setStaffData([...staffData, data]);
  }

  function addDate(index) {
    staffData[index.index].preferences.push("");
    setStaffData([...staffData]);
  }

  function removeStaffMember(index) {
    staffData.splice(index.index, 1);
    setStaffData([...staffData]);
  }

  return (
    <div className="App">
      <h1 className="App-header"> Residence Life Auto Duty Scheduler </h1>
      <Container className="Form-Format">
        <Form onSubmit={(formEvent) => sendFormData(formEvent)}>
          <Form.Label
            className="Scheduling-options"
            style={{ marginBottom: "20px" }}
          >
            Duty Scheduling Options
          </Form.Label>
          <Form.Row className="RD-duty-checkbox">
            <Form.Check
              type="checkBox"
              label="RD Duty (Leave Unchecked for RA Duty)"
              className="doubleDuty-checkBox"
              onClick={() =>
                setFormData({
                  ...formData,
                  raDuty: !formData.raDuty,
                })
              }
            />
          </Form.Row>
          <Form.Row>
            <Form.Group>
              <Form.Label>Start Date</Form.Label>
              <Form.Control
                type="date"
                required="True"
                onChange={(inputEvent) =>
                  setFormData({
                    ...formData,
                    startDate: inputEvent.target.value,
                  })
                }
              ></Form.Control>
            </Form.Group>

            <Form.Group>
              <Col xs={"auto"}>
                <Form.Label>End Date</Form.Label>
                <Form.Control
                  required="True"
                  type="date"
                  onChange={(inputEvent) =>
                    setFormData({
                      ...formData,
                      endDate: inputEvent.target.value,
                    })
                  }
                ></Form.Control>
              </Col>
            </Form.Group>
          </Form.Row>
          <Form.Row>
            <Form.Group className="input-box">
              <Form.Control
                type="text"
                placeholder="Enter Hall Name"
                onChange={(inputEvent) =>
                  setFormData({ ...formData, hall: inputEvent.target.value })
                }
                value={formData.hall}
              />
            </Form.Group>
            <Form.Group>
              <Col xs={"auto"}>
                <Form.Check
                  type="checkBox"
                  label="Weekend Double Duty"
                  className="doubleDuty-checkBox"
                  onClick={() =>
                    setFormData({
                      ...formData,
                      doubleDuty: !formData.doubleDuty,
                    })
                  }
                />
              </Col>
            </Form.Group>
          </Form.Row>
          <Form.Label
            className="Staff-members"
            style={{ marginBottom: "15px" }}
          >
            Staff Members{" "}
          </Form.Label>
          {formData["raDuty"] === false && (
            <p style={{ fontSize: 18 }}>
              Please enter in the date of the specific shift you do not want to
              sit. <br />
              For example week 1 starts on Jan 18 so you would input Jan 18.{" "}
              <br />
            </p>
          )}
          {staffData.map((data, index) => (
            <React.Fragment>
              <Form.Row>
                <Form.Group key={index} className="input-box">
                  <Form.Label> Name </Form.Label>

                  <Form.Control
                    type="text"
                    required="True"
                    placeholder="Enter staff member"
                    onChange={(inputEvent) =>
                      setStaffData(
                        staffData.map((item, index2) =>
                          index === index2
                            ? {
                                ...staffData[index],
                                name: inputEvent.target.value,
                              }
                            : item
                        )
                      )
                    }
                    value={staffData[index].name}
                  />
                </Form.Group>
                <Form.Group className="sra-checkbox">
                  <Col xs={"auto"}>
                    <Form.Check
                      type="checkBox"
                      label="SRA"
                      className="sra-checkBox"
                      onClick={() =>
                        setStaffData(
                          staffData.map((item, index2) =>
                            index === index2
                              ? {
                                  ...staffData[index],
                                  SRA: true,
                                }
                              : item
                          )
                        )
                      }
                    />
                  </Col>
                </Form.Group>
              </Form.Row>
              <Form.Label>{formData['raDuty'] === true ? "Days" : "Weeks"} Cannot Sit</Form.Label>
              <Form.Row>
                {staffData[index].preferences.map((input, index2) => (
                  <React.Fragment>
                    <Col xs="auto">
                      <Form.Group key={index}>
                        <Form.Control
                          type="date"
                          onChange={(inputEvent) =>
                            setStaffData(
                              staffData.map((item, index3) =>
                                index === index3
                                  ? {
                                      ...staffData[index],
                                      preferences: item.preferences.map(
                                        (item2, index4) =>
                                          index2 === index4
                                            ? inputEvent.target.value
                                            : item2
                                      ),
                                    }
                                  : item
                              )
                            )
                          }
                          value={staffData[index].preferences[index2]}
                        />
                      </Form.Group>
                    </Col>
                  </React.Fragment>
                ))}
                <Col>
                  <Button
                    variant="secondary"
                    className="btn.btn-secondary"
                    onClick={() => addDate({ index })}
                  >
                    Add date
                  </Button>
                </Col>
              </Form.Row>
              <Form.Row>
                <Col>
                  <Button
                    variant="danger"
                    onClick={() => removeStaffMember({ index })}
                    style={{ marginBottom: "35px" }}
                  >
                    Remove Staff Member
                  </Button>
                </Col>
              </Form.Row>
            </React.Fragment>
          ))}

          <Form.Row className="submit-row">
            <Form.Group>
              <Button variant="primary" type="submit" disabled={isLoading}>
                {isLoading ? 'Loading...' : 'Submit'}
              </Button>
            </Form.Group>
            <Form.Group>
              <Col>
                <Button variant="secondary" onClick={addStaffMember}>
                  Add staff member
                </Button>
              </Col>
            </Form.Group>
          </Form.Row>
        </Form>
      </Container>

      <footer className="Footer"> &copy; Pharez J. Varlack </footer>
    </div>
  );
}

export default App;

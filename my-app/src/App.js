import React, { Fragment, useState } from "react";
import DatePicker from "react-datepicker";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import AppendForm from "./appendForm";
import Card from "react-bootstrap/Card";
import Dropdown from "react-bootstrap/Dropdown";

function App() {
  let [formData, setFormData] = useState([{}]);
  let [staffData, setStaffData] = useState({
    name: "",
    preferences: {},
  });

  let [date, setDate] = useState([]);
  let [startDate, setStartDate] = useState();
  let [endDate, setEndDate] = useState();

  const sendFormData = async (formEvent) => {
    formEvent.preventDefault();
    console.log(formEvent);
    const requestOptions = {
      method: "POST",
      body: JSON.stringify(formData),
    };

    let response = await fetch(
      "https://localhost:8000/schedule_duty",
      requestOptions
    );

    setFormData({ video_link: "" });
  };
  
  function appendFormData() {
    setFormData([...formData, staffData]);
    setStaffData({ name: "", hall: "" });
        console.log(formData);

  }

  function appendDates(){
    console.log(staffData)
    let i;
    for (i=startDate; i<=endDate; i++) {
      setDate(date.push({[i]: []}))
    }
  }
  //we can just say completed

  return (
    <Container>
      <Form className="mt-5" onSubmit={(formEvent) => sendFormData(formEvent)}>
        <Form.Label>Duty Schedule Options</Form.Label>
        <Form.Row>
          <Form.Group>
            <Col xs={"auto"}>
              <Form.Label>First Month</Form.Label>
              <Form.Control
                as="select"
                custom
                onChange={(inputEvent) => setStartDate(inputEvent.target.value)}
              >
                <option value="0"> Choose </option>
                <option value="1"> January </option>
                <option value="2"> February </option>
                <option value="3"> March </option>
                <option value="4"> April </option>
                <option value="5"> May </option>
                <option value="6"> June </option>
                <option value="7"> July </option>
                <option value="8"> August </option>
                <option value="9"> September </option>
                <option value="10"> October </option>
                <option value="11"> November </option>
                <option value="12"> December </option>
              </Form.Control>
            </Col>
          </Form.Group>

          <Form.Group>
            <Col xs={"auto"}>
              <Form.Label>Last Month</Form.Label>
              <Form.Control
                as="select"
                custom
                onChange={(inputEvent) => setEndDate(inputEvent.target.value)}
              >
                <option value="0"> Choose </option>
                <option value="1"> January </option>
                <option value="2"> February </option>
                <option value="3"> March </option>
                <option value="4"> April </option>
                <option value="5"> May </option>
                <option value="6"> June </option>
                <option value="7"> July </option>
                <option value="8"> August </option>
                <option value="9"> September </option>
                <option value="10"> October </option>
                <option value="11"> November </option>
                <option value="12"> December </option>
              </Form.Control>
            </Col>
          </Form.Group>
                  <Button variant="primary" size="sm" onClick={appendDates}>
          Confirm
        </Button>
        </Form.Row>
        <Form.Group>
          <Form.Control
            type="url"
            placeholder="Enter Hall Name"

            onChange={(inputEvent) =>
              setFormData([...formData, 0: { hall: inputEvent.target.value }])
            }
            value={formData.hall}
          />
        </Form.Group>
        {formData.map((data, index) => (
          <React.Fragment>
            <Form.Group key={index}>
            <Form.Label> Name </Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter staff member name"
                onChange={(inputEvent) =>

                  setFormData([...formData, data ])
                }
              />
            </Form.Group>

            <Form.Row>
              <Form.Group>
                <Col xs={"auto"}>
                  <Form.Label> Dates </Form.Label>
                  <Form.Control placeholder="Enter dates seperated by a comma" 
                  type="text"
                  placeholder="Enter dates"
                  onChange={(inputEvent) =>
                    setFormData([{ ...formData, [index]: {...formData.index, "date":inputEvent.target.value, } }])
                  }/>
                </Col>
              </Form.Group>
            </Form.Row>
          </React.Fragment>
        ))}

        <Button variant="primary" type="submit">
          Submit
        </Button>

        <Button variant="secondary" onClick={appendFormData}>
          add staff member
        </Button>
      </Form>
    </Container>
  );
}

export default App;
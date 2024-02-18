import Navbar from '../components/Navbar';
import Editor from '../components/Editor';
import Console from '../components/Console';
import FileInput from '../components/FileInput';
import SaveFileButton from '../components/SaveFileButton';
import RunInputButton from '../components/RunInputButton';
import { useState } from 'react';

function Index() {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('$');

  return (
    <div class="container-fluid">
      <div class="row">
        <div class="col-12" style={{ padding: "0px" }}>
          <Navbar />
        </div>
      </div>
      <div class="row">
        <div class="col-4" style={{ padding: "10px 0px 10px 15px" }}>
          <FileInput {...{ setInput }} />
        </div>
        <div class="col-1" style={{ padding: "10px 5px 10px 15px" }}>
          <SaveFileButton {...{ input }} />
        </div>
        <div class="col-1" style={{ padding: "10px 15px 10px 5px" }}>
          <RunInputButton {...{ input, setOutput }} />
        </div>
        <div class="col-6" style={{ padding: "10px 15px 10px 0px" }}>
          <div
            class="badge"
            style={{
              display: "flex",
              alignItems: "center",
              height: "100%",
              backgroundColor: "rgba(108, 117, 125, 0.5)",
              color: "#d4d4d4",
              fontSize: "16px",
            }}
          >
            Consola
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-6" style={{ padding: "0px" }}>
          <Editor {...{ input, setInput }} />
        </div>
        <div class="col-6" style={{ padding: "0px" }}>
          <Console {...{ output }} />
        </div>
      </div>
    </div>
  );
}

export default Index;

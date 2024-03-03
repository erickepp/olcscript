import axios from 'axios';
const serverIP = process.env.REACT_APP_SERVER_IP;

function RunCodeButton({ input, setOutput }) {
  
  const handleRunCode = async () => {
    const run = document.getElementById('run');
    const spinner = document.getElementById('spinner');

    run.hidden = true;
    spinner.hidden = false;
    setOutput('');
    
    try {
      const { data } = await axios.post(`${serverIP}/interpreter`, { input }, {
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 15000
      });

      localStorage.setItem('errors', JSON.stringify(data.errors));
      localStorage.setItem('symbolTable', JSON.stringify(data.symbolTable));
      setOutput(data.output);
    } catch (error) {
      setOutput(error.stack);
    }

    run.hidden = false;
    spinner.hidden = true;
  };

  return (
    <button
      type="button"
      class="btn btn-primary"
      style={{ width: "100%", overflow: "hidden" }}
      onClick={handleRunCode}
    >
      <span id="run">Ejecutar</span>
      <span
        class="spinner-border spinner-border-sm"
        aria-hidden="true"
        id="spinner"
        hidden
      >
      </span>
    </button>
  );
  
}

export default RunCodeButton;

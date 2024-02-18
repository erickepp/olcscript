function FileInput({ setInput }) {

  const handleOpenFile = (event) => {
    try {
      const file = event.target.files[0];

      if (file) {
        const reader = new FileReader();

        reader.onload = (e) => {
          const content = e.target.result;
          setInput(content);
        };

        reader.readAsText(file);
      }
    } catch (error) {
      console.error('Error al leer el archivo:', error);
    }
  };

  return (
    <input 
      className="form-control"
      type="file"
      id="formFile"
      data-bs-theme="dark"
      style={{ width: "100%" }}
      onChange={handleOpenFile}
      accept=".olc"
    />
  );
  
}

export default FileInput;

function SaveFileButton({ input }) {

  const handleSaveFile = async () => {
    try {
      const handle = await window.showSaveFilePicker({
        suggestedName: 'file.olc',
        types: [{
          description: 'Text file',
          accept: { 'text/plain': ['.olc'] },
        }]
      });
      const writable = await handle.createWritable();
      await writable.write(input);
      await writable.close();
    } catch (err) {
      console.error(err.name, err.message);
    }
  };

  return (
    <button
      type="button"
      class="btn btn-secondary"
      style={{ width: "100%", overflow: "hidden" }}
      onClick={handleSaveFile}
    >
      Guardar
    </button>
  );
  
}

export default SaveFileButton;

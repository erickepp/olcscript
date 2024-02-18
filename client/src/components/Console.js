function Console({ output }) {
  return (
    <div
      style={{
        height: "80vh",
        padding: "0px 10px 10px 10px",
        backgroundColor: "#1c1c1c",
        color: "#d4d4d4",
        fontFamily: "Consolas, 'Courier New', monospace",
        fontSize: "14px",
        overflowY: "auto",
        whiteSpace: "pre-line"
      }}
    >
      {output}
    </div>
  );
}

export default Console;

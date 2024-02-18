import MonacoEditor from '@monaco-editor/react';

function Editor({ input, setInput }) {
  return (
    <MonacoEditor
      height="80vh"
      defaultLanguage="typescript"
      value={input}
      onChange={value => { setInput(value) }}
      theme="vs-dark"
    />
  );
}

export default Editor;

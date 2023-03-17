import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <div className="App">
      <Button variant="primary">Flash an application</Button>{' '}
      <Button variant="primary">Flash a workspace</Button>{' '}
      <Button variant="primary">Flash a binary</Button>{' '}
    </div>
  );
}

export default App;

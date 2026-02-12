import { Routes, Route } from "react-router-dom";
import Landing from "./pages/Landing";
import UploadResume from "./pages/UploadResume";
import Aptitude from "./pages/Aptitude";
import Technical from "./pages/Technical";

function App() {
  return (
    
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/upload" element={<UploadResume />} />
      <Route path="/aptitude" element={<Aptitude />} />
      <Route path="/technical" element={<Technical />} />
    </Routes>
  );
}

export default App;

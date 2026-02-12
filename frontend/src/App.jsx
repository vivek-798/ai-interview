import { Routes, Route } from "react-router-dom";
import Landing from "./pages/Landing";
import UploadResume from "./pages/UploadResume";
import Aptitude from "./pages/Aptitude";
import Technical from "./pages/Technical";
import HR from "./pages/HR";
// import FinalReport from "./pages/FinalReport";
import Final from "./pages/Final"; 

function App() {
  return (
    
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/upload" element={<UploadResume />} />
      <Route path="/aptitude" element={<Aptitude />} />
      <Route path="/technical" element={<Technical />} />
      <Route path="/hr" element={<HR />} />
       <Route path="/final" element={<Final />} />

    </Routes>
  );
}

export default App;

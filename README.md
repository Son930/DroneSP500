<h1>DroneConnector for SNAPTAIN SP500</h1>
<h2>WARNING! THIS IS STILL A WORK IN PROGRESS!</h2>
<p><strong>DroneConnector</strong> is a Python-based application for controlling a drone over Wi-Fi using a TCP/UDP communication protocol. The project leverages Joy-Con controllers for intuitive control and provides a dynamic interface for drone commands.</p>
    
<h2>Features</h2>
<ul>
    <li>Control a drone using Nintendo Joy-Con controllers.</li>
    <li>Real-time command transmission over TCP/UDP.</li>
    <li>Modular code structure for adding new features.</li>
    <li>Logging and debugging support for easy troubleshooting.</li>
</ul>

<h2>Requirements</h2>
<ul>
  <li>SNAPTAIN SP500 (Drone)</li>
  <li>Nintendo JoyCon</li>
    <li><strong>Python 3.8+</strong></li>
    <li>Libraries:
        <ul>
            <li><code>pyjoycon</code> (for Joy-Con integration)</li>
            <li><code>socket</code> (for network communication)</li>
            <li><code>time</code> (for delays and timing operations)</li>
        </ul>
    </li>
  
</ul>
<p>Install dependencies using:</p>
<pre><code>pip install --insert name library</code></pre>

<h2>Setup</h2>

  <h3>1. Clone the Repository</h3>

  <h3>2. Connect Joy-Con Controllers</h3>
  <p>Ensure Joy-Con controllers are paired with your system. The application will automatically detect connected controllers.</p>

  <h3>3. Configure Drone Network</h3>
  <p>Connect your machine to the drone's Wi-Fi network. Update <code>drone_ip</code> and <code>drone_port</code> in <code>main.py</code> with the correct IP and port of the drone.</p>

  <h2>Usage</h2>

  <h3>Run the Application</h3>
  <pre><code>python main.py</code></pre>

  <h3>Send Commands to Drone</h3>
  <p>Use Joy-Con controllers to send commands dynamically. Default controls include:</p>
  <ul>
      <li>Left Joy-Con: Movement and rotation.</li>
      <li>Right Joy-Con: Throttle and altitude adjustments.</li>
      <li>Right Plus button: Emergency stop</li>
      <li>Button L (left joycon): Next lvl of speed</li>
      <li>Button R (right joycon): Flip command</li>
      <li>Button UP (left  joycon): Trim Forward</li>
      <li>Button LEFT (left  joycon): Trim LEFT</li>
      <li>Button RIGHT (left  joycon): Trim RIGHT</li>
      <li>Button DOWN (left  joycon): Trim DOWN</li>
      <li>Buton ZL (left joycon): Landing Sequence (work in progress)</li>
      <li>Button Home (right joycon): Take Off sequence</li>
  </ul>

 
  <h2>Troubleshooting</h2>
  <ul>
      <li><strong>Joy-Con not detected:</strong>
          <ul>
              <li>Ensure Joy-Cons are paired with your system.</li>
              <li>Run <code>pyjoycon</code> diagnostics to verify connection.</li>
          </ul>
      </li>
      <li><strong>No response from drone:</strong>
          <ul>
              <li>Verify the drone's IP and port.</li>
              <li>Check if the drone is in command mode.</li>
          </ul>
      </li>
  </ul>

  <h2>Contributing</h2>
  <p>Contributions are welcome! Please follow these steps:</p>
  <ol>
      <li>Fork the repository.</li>
      <li>Create a feature branch (<code>git checkout -b feature-name</code>).</li>
      <li>Commit your changes (<code>git commit -m "Add feature-name"</code>).</li>
      <li>Push to the branch (<code>git push origin feature-name</code>).</li>
      <li>Open a pull request.</li>
  </ol>

  <h2>License</h2>
  <p>This project is licensed under the MIT License. See the <code>LICENSE</code> file for details.</p>

  <h2>Acknowledgments</h2>
  <ul>
      <li>Special thanks to the developers of <code>pyjoycon</code> for their Joy-Con integration tools.</li>
      <li>Inspired by the growing demand for accessible drone control applications.</li>
  </ul>


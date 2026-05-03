import '../css/About.css';
import { FaCamera, FaCar, FaBell, FaChartBar, FaLightbulb, FaLock } from 'react-icons/fa';

function About() {
  return (
    <div className="about-container">
      <div className="about-header">
        <h1>About Police Fine Management System</h1>
        <p className="tagline">Modernizing Traffic Law Enforcement</p>
      </div>

      <div className="about-content">
        {/* Overview Section */}
        <section className="about-section">
          <div className="section-header">
            <h2>Overview</h2>
          </div>
          <p>
            The Police Fine Management System is a digital platform designed to streamline
            traffic violation management. It enables law enforcement officers to instantly
            issue fines online with photographic proof, making the process faster, more
            transparent, and easier to track.
          </p>
        </section>

        {/* Mission Section */}
        <section className="about-section">
          <div className="section-header">
            <h2>Our Mission</h2>
          </div>
          <p>
            To enhance road safety and improve traffic law enforcement by providing law
            enforcement agencies with a modern, efficient, and user-friendly digital platform
            that ensures accountability and direct communication with traffic violators.
          </p>
        </section>

        {/* How It Works */}
        <section className="about-section">
          <div className="section-header">
            <h2>How It Works</h2>
          </div>
          <div className="steps-container">
            <div className="step">
              <div className="step-number">1</div>
              <h3>Capture Evidence</h3>
              <p>
                Officers click a photo of the violation as proof. This ensures documentation
                and accountability.
              </p>
            </div>

            <div className="step">
              <div className="step-number">2</div>
              <h3>Enter Vehicle Details</h3>
              <p>
                Input the vehicle number plate. Our system automatically fetches registered
                owner details including vehicle type and model.
              </p>
            </div>

            <div className="step">
              <div className="step-number">3</div>
              <h3>Document the Violation</h3>
              <p>
                Write a detailed explanation of the traffic violation for the record and
                violation database.
              </p>
            </div>

            <div className="step">
              <div className="step-number">4</div>
              <h3>Set Fine Amount</h3>
              <p>
                Enter the applicable fine amount based on traffic laws and violation severity.
              </p>
            </div>

            <div className="step">
              <div className="step-number">5</div>
              <h3>Issue & Notify</h3>
              <p>
                Submit the fine. The vehicle owner receives an instant notification via
                Nagarik App with complete violation details.
              </p>
            </div>

            <div className="step">
              <div className="step-number">6</div>
              <h3>Track & Manage</h3>
              <p>
                All fines are tracked digitally, creating a permanent record for the vehicle
                and ensuring transparency.
              </p>
            </div>
          </div>
        </section>

        {/* Key Features */}
        <section className="about-section">
          <div className="section-header">
            <h2>Key Features</h2>
          </div>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon"><FaCamera /></div>
              <h3>Photo Evidence</h3>
              <p>Upload clear photographic proof of traffic violations for documentation</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon"><FaCar /></div>
              <h3>Vehicle Lookup</h3>
              <p>Instant access to registered vehicle owner details via number plate</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon"><FaBell /></div>
              <h3>Direct Notification</h3>
              <p>Send fines directly to violators via Nagarik App for instant awareness</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon"><FaChartBar /></div>
              <h3>Digital Record</h3>
              <p>Maintain comprehensive digital records of all issued fines for analysis</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon"><FaLightbulb /></div>
              <h3>Real-time Processing</h3>
              <p>Instantly process and issue fines without paperwork delays</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon"><FaLock /></div>
              <h3>Secure & Transparent</h3>
              <p>Secure data handling with complete transparency in violation documentation</p>
            </div>
          </div>
        </section>

        {/* Benefits Section */}
        <section className="about-section">
          <div className="section-header">
            <h2>Benefits</h2>
          </div>
          <div className="benefits-list">
            <div className="benefit-item">
              <h3>For Law Enforcement</h3>
              <ul>
                <li>Faster fine issuance process</li>
                <li>Digital documentation and record keeping</li>
                <li>Reduced administrative burden</li>
                <li>Better data analytics and reporting</li>
                <li>Improved accountability and transparency</li>
              </ul>
            </div>

            <div className="benefit-item">
              <h3>For Vehicle Owners</h3>
              <ul>
                <li>Instant notification of violations</li>
                <li>Clear photographic evidence of violations</li>
                <li>Detailed explanation of violations</li>
                <li>Digital payment options</li>
                <li>Transparent fine calculation</li>
              </ul>
            </div>

            <div className="benefit-item">
              <h3>For Society</h3>
              <ul>
                <li>Improved road safety awareness</li>
                <li>Reduced traffic violations</li>
                <li>Better data for traffic management</li>
                <li>Reduced corruption in fining process</li>
                <li>More efficient use of law enforcement resources</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Technology Section */}
        <section className="about-section">
          <div className="section-header">
            <h2>Technology</h2>
          </div>
          <div className="tech-stack">
            <div className="tech-item">
              <h3>Frontend</h3>
              <p>React.js with modern UI/UX design</p>
            </div>
            <div className="tech-item">
              <h3>Backend</h3>
              <p>Django REST API for secure data handling</p>
            </div>
            <div className="tech-item">
              <h3>Integration</h3>
              <p>Nagarik App API for direct notifications</p>
            </div>
            <div className="tech-item">
              <h3>Database</h3>
              <p>Secure database for fine records and vehicle information</p>
            </div>
          </div>
        </section>

        {/* Contact Section */}
        <section className="about-section last-section">
          <div className="section-header">
            <h2>Questions or Feedback?</h2>
          </div>
          <p>
            Have questions about the Police Fine Management System or want to provide feedback?
            Please visit our <a href="/contact">Contact Page</a> to get in touch with us.
          </p>
        </section>
      </div>
    </div>
  );
}

export default About;

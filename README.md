# SentinelLink
SentinelLink: Zero-Trust Anti-Phishing Ecosystem 

SentinelLink is a proactive "Digital Bodyguard" designed to protect users from the "Golden Hour" of cybercrime—the critical window before a scam link is blacklisted.

 The Vision
To move beyond passive warnings and create a "Zero-Trust" browsing layer. By utilizing Remote Browser Isolation (RBI), we ensure that malicious code never touches the user's hardware.

 Key Features
Air-Gapped Rendering (RBI): Instead of opening a link on your device, our Python backend "detonates" it on a safe server. We stream only a visual "picture" (pixels) of the site to the user, physically blocking any script execution or malware "jumps".

Military-Grade Decoys (Honey-Tokens): A "Smart-Fill" feature that generates realistic but fake Aadhaar or UPI data. This baits the scammer into revealing their intent without risking the user's real identity.

Aviation Blackbox (Forensics): Automatically generates a Forensic PDF Report. It captures hidden metadata like Server IP, SSL age, and hosting provider, providing "Chain of Custody" evidence for the Cyber Cell or Chakshu facility.

NLP Intent Analysis: Our engine scans for "Pay-to-Work" or "Refundable Deposit" keywords, identifying the intent of a scam even if the site is brand new and not blacklisted.

🛠️ Technical Stack
Backend: Python (FastAPI) & Playwright for headless browser automation.

Frontend: Manifest V3 Browser Extension (JavaScript) for real-time link interception.

Blockchain: Quai Network for anchoring evidence integrity.

Intelligence: NLTK/TextBlob for Linguistic Intelligence.

📈 Future Scope & Scalability
Distribution: Deployment as a high-performance Browser Extension for Chrome and Edge to provide a zero-friction overlay in WhatsApp/Telegram Web.

Strategic Tie-ups: * ISPs/Telecoms: Potential integration as a value-added "Clean Pipe" safety layer (e.g., Airtel/Jio).

Govt Integration: Feeding real-time threat intelligence to the National Cyber Crime Reporting Portal (NCRP).

Monetization: B2B licensing for Universities and HR firms to protect their brands from "Cloning" scams.

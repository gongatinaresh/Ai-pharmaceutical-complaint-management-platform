import { useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import "./App.css";

import {
  updateField,
  populateFromAI,
  setAIResult,
  setProcessing,
  setError,
  resetComplaint,
} from "./store/complaintSlice";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function App() {
  const dispatch = useDispatch();
  const complaint = useSelector((state) => state.complaint);

  const fileInputRef = useRef(null);

  const [pasteText, setPasteText] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleChange = (field, value) => {
    dispatch(
      updateField({
        field,
        value,
      })
    );
  };

  // ---------------------------------------
  // Process AI result
  // ---------------------------------------
  const handleAIResult = (result) => {
    const extractedData = result?.extracted_data || {};

    // Populate complaint form
    dispatch(populateFromAI(extractedData));

    // Populate AI analysis
    dispatch(setAIResult(result));

    setMessage("AI processing completed successfully.");
  };

  // ---------------------------------------
  // Process pasted complaint
  // ---------------------------------------
  const handleProcessText = async () => {
    if (!pasteText.trim()) {
      dispatch(setError("Please enter complaint text first."));
      setMessage("Please enter complaint text first.");
      return;
    }

    dispatch(setProcessing(true));
    dispatch(setError(null));
    setMessage("AI is processing the complaint...");

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/ai/process`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            complaint_text: pasteText,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Complaint processing failed."
        );
      }

      handleAIResult(data.ai_result);

    } catch (error) {
      console.error(error);

      dispatch(setError(error.message));
      setMessage(`Error: ${error.message}`);

    } finally {
      dispatch(setProcessing(false));
    }
  };

  // ---------------------------------------
  // File selection
  // ---------------------------------------
  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setSelectedFile(file);
    setMessage(`Selected file: ${file.name}`);
  };

  // ---------------------------------------
  // Upload document
  // ---------------------------------------
  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage("Please select a complaint document first.");
      return;
    }

    if (selectedFile.size > 10 * 1024 * 1024) {
      setMessage("File size must be less than 10 MB.");
      return;
    }

    dispatch(setProcessing(true));
    dispatch(setError(null));
    setMessage("AI is reading and processing the document...");

    try {
      const formData = new FormData();

      formData.append("file", selectedFile);

      const response = await fetch(
        `${API_BASE_URL}/api/upload/complaint`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Document processing failed."
        );
      }

      handleAIResult(data.ai_result);

    } catch (error) {
      console.error(error);

      dispatch(setError(error.message));
      setMessage(`Error: ${error.message}`);

    } finally {
      dispatch(setProcessing(false));
    }
  };

  // ---------------------------------------
  // Save complaint
  // ---------------------------------------
  const handleSaveComplaint = async () => {
    if (!complaint.detailed_description?.trim()) {
      setMessage(
        "Please provide a detailed complaint description."
      );
      return;
    }

    dispatch(setProcessing(true));
    dispatch(setError(null));
    setMessage("Saving complaint...");

    try {
      const payload = {
        complaint_source:
          complaint.complaint_source || null,

        customer_name:
          complaint.customer_name || null,

        product_name:
          complaint.product_name || null,

        product_strength_grade:
          complaint.product_strength_grade || null,

        batch_number:
          complaint.batch_number || null,

        manufacturing_date:
          complaint.manufacturing_date || null,

        expiry_date:
          complaint.expiry_date || null,

        quantity_affected:
          complaint.quantity_affected
            ? Number(complaint.quantity_affected)
            : null,

        complaint_type:
          complaint.complaint_type || null,

        complaint_date:
          complaint.complaint_date || null,

        detailed_description:
          complaint.detailed_description || null,

        initial_severity:
          complaint.initial_severity ||
          complaint.severity ||
          null,

        priority:
          complaint.priority || null,
      };

      const response = await fetch(
        `${API_BASE_URL}/api/complaints/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to save complaint."
        );
      }

      setMessage(
        `Complaint saved successfully. Complaint ID: ${data.complaint_id}`
      );

    } catch (error) {
      console.error(error);

      dispatch(setError(error.message));
      setMessage(`Error: ${error.message}`);

    } finally {
      dispatch(setProcessing(false));
    }
  };

  // ---------------------------------------
  // Reset
  // ---------------------------------------
  const handleReset = () => {
    dispatch(resetComplaint());

    setPasteText("");
    setSelectedFile(null);
    setMessage("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">
        <div>
          <h1>Pharma Complaint AI</h1>
          <p>AI Complaint Management System</p>
        </div>

        <span className="status">
          ● {complaint.status}
        </span>
      </header>


      {/* MAIN */}
      <main className="main-container">

        {/* =====================================
            LEFT PANEL
        ====================================== */}
        <section className="complaint-panel">

          <div className="panel-title">
            <h2>Log Customer Complaint</h2>
            <span>Complaint Intake</span>
          </div>


          {/* 1. ORIGIN */}
          <div className="section">

            <h3>1. Origin & Customer Details</h3>

            <div className="form-grid">

              <div className="form-group">
                <label>Complaint Source</label>

                <select
                  value={complaint.complaint_source}
                  onChange={(e) =>
                    handleChange(
                      "complaint_source",
                      e.target.value
                    )
                  }
                >
                  <option value="">
                    Select source
                  </option>

                  <option value="Email">
                    Email
                  </option>

                  <option value="Phone">
                    Phone
                  </option>

                  <option value="Website">
                    Website
                  </option>

                  <option value="Distributor">
                    Distributor
                  </option>

                  <option value="Other">
                    Other
                  </option>

                </select>
              </div>


              <div className="form-group">

                <label>Customer Name</label>

                <input
                  type="text"
                  value={complaint.customer_name}
                  onChange={(e) =>
                    handleChange(
                      "customer_name",
                      e.target.value
                    )
                  }
                  placeholder="Enter customer name"
                />

              </div>

            </div>

          </div>


          {/* 2. PRODUCT */}
          <div className="section">

            <h3>2. Product & Batch Identification</h3>

            <div className="form-grid">

              <div className="form-group">

                <label>Product Name</label>

                <input
                  type="text"
                  value={complaint.product_name}
                  onChange={(e) =>
                    handleChange(
                      "product_name",
                      e.target.value
                    )
                  }
                  placeholder="Enter product name"
                />

              </div>


              <div className="form-group">

                <label>
                  Product Strength / Grade
                </label>

                <input
                  type="text"
                  value={
                    complaint.product_strength_grade
                  }
                  onChange={(e) =>
                    handleChange(
                      "product_strength_grade",
                      e.target.value
                    )
                  }
                  placeholder="Enter strength or grade"
                />

              </div>


              <div className="form-group">

                <label>Batch Number</label>

                <input
                  type="text"
                  value={complaint.batch_number}
                  onChange={(e) =>
                    handleChange(
                      "batch_number",
                      e.target.value
                    )
                  }
                  placeholder="Enter batch number"
                />

              </div>


              <div className="form-group">

                <label>Manufacturing Date</label>

                <input
                  type="date"
                  value={
                    complaint.manufacturing_date || ""
                  }
                  onChange={(e) =>
                    handleChange(
                      "manufacturing_date",
                      e.target.value
                    )
                  }
                />

              </div>


              <div className="form-group">

                <label>Expiry Date</label>

                <input
                  type="date"
                  value={
                    complaint.expiry_date || ""
                  }
                  onChange={(e) =>
                    handleChange(
                      "expiry_date",
                      e.target.value
                    )
                  }
                />

              </div>


              <div className="form-group">

                <label>Quantity Affected</label>

                <input
                  type="number"
                  value={
                    complaint.quantity_affected || ""
                  }
                  onChange={(e) =>
                    handleChange(
                      "quantity_affected",
                      e.target.value
                    )
                  }
                  placeholder="Enter quantity"
                />

              </div>

            </div>

          </div>


          {/* 3. COMPLAINT */}
          <div className="section">

            <h3>3. Complaint Details</h3>

            <div className="form-grid">

              <div className="form-group">

                <label>Complaint Type</label>

                <select
                  value={complaint.complaint_type}
                  onChange={(e) =>
                    handleChange(
                      "complaint_type",
                      e.target.value
                    )
                  }
                >

                  <option value="">
                    Select type
                  </option>

                  <option value="Product Quality">
                    Product Quality
                  </option>

                  <option value="Packaging">
                    Packaging
                  </option>

                  <option value="Labeling">
                    Labeling
                  </option>

                  <option value="Delivery">
                    Delivery
                  </option>

                  <option value="Documentation">
                    Documentation
                  </option>

                  <option value="Adverse Event">
                    Adverse Event
                  </option>

                  <option value="Other">
                    Other
                  </option>

                </select>

              </div>


              <div className="form-group">

                <label>Complaint Date</label>

                <input
                  type="date"
                  value={
                    complaint.complaint_date || ""
                  }
                  onChange={(e) =>
                    handleChange(
                      "complaint_date",
                      e.target.value
                    )
                  }
                />

              </div>

            </div>


            <div className="form-group">

              <label>
                Detailed Complaint Description
              </label>

              <textarea
                rows="5"
                value={
                  complaint.detailed_description
                }
                onChange={(e) =>
                  handleChange(
                    "detailed_description",
                    e.target.value
                  )
                }
                placeholder="Enter detailed complaint description"
              />

            </div>

          </div>


          {/* 4. ASSESSMENT */}
          <div className="section">

            <h3>
              4. Initial Assessment & Priority
            </h3>

            <div className="form-grid">

              <div className="form-group">

                <label>Initial Severity</label>

                <select
                  value={
                    complaint.initial_severity ||
                    complaint.severity ||
                    ""
                  }
                  onChange={(e) =>
                    handleChange(
                      "initial_severity",
                      e.target.value
                    )
                  }
                >

                  <option value="">
                    Select severity
                  </option>

                  <option value="Minor">
                    Minor
                  </option>

                  <option value="Major">
                    Major
                  </option>

                  <option value="Critical">
                    Critical
                  </option>

                </select>

              </div>


              <div className="form-group">

                <label>Priority</label>

                <select
                  value={complaint.priority}
                  onChange={(e) =>
                    handleChange(
                      "priority",
                      e.target.value
                    )
                  }
                >

                  <option value="">
                    Select priority
                  </option>

                  <option value="Low">
                    Low
                  </option>

                  <option value="Medium">
                    Medium
                  </option>

                  <option value="High">
                    High
                  </option>

                  <option value="Critical">
                    Critical
                  </option>

                </select>

              </div>

            </div>

          </div>


          {/* BUTTONS */}
          <div className="form-actions">

            <button
              className="reset-btn"
              onClick={handleReset}
              disabled={complaint.isProcessing}
            >
              Reset Form
            </button>


            <button
              className="save-btn"
              onClick={handleSaveComplaint}
              disabled={complaint.isProcessing}
            >
              {complaint.isProcessing
                ? "Processing..."
                : "Save Complaint"}
            </button>

          </div>

        </section>


        {/* =====================================
            RIGHT PANEL
        ====================================== */}
        <section className="ai-panel">

          <div className="ai-header">

            <div>

              <h2>
                AI Complaint Intake Assistant
              </h2>

              <p>
                Upload or paste a complaint and let
                AI extract the details.
              </p>

            </div>

          </div>


          {/* UPLOAD */}
          <div className="upload-box">

            <div className="upload-icon">
              ↑
            </div>

            <h3>
              Upload Complaint Document
            </h3>

            <p>
              Drag & drop or browse your complaint
              document
            </p>

            <p className="file-types">
              PDF, DOCX, TXT, EML • Maximum 10 MB
            </p>


            {/* Hidden input */}
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.docx,.txt,.eml"
              onChange={handleFileChange}
              style={{ display: "none" }}
            />


            <button
              className="browse-btn"
              onClick={() =>
                fileInputRef.current?.click()
              }
              disabled={complaint.isProcessing}
            >
              Browse Files
            </button>


            {selectedFile && (
              <p className="selected-file">
                📄 {selectedFile.name}
              </p>
            )}


            {selectedFile && (
              <button
                className="process-btn"
                onClick={handleUpload}
                disabled={complaint.isProcessing}
              >
                {complaint.isProcessing
                  ? "Processing Document..."
                  : "Process Uploaded Document"}
              </button>
            )}

          </div>


          {/* TEXT INPUT */}
          <div className="ai-section">

            <h3>
              Or Paste Complaint Text
            </h3>

            <textarea
              rows="7"
              value={pasteText}
              onChange={(e) =>
                setPasteText(e.target.value)
              }
              placeholder="Paste customer complaint, email or message here..."
            />


            <button
              className="process-btn"
              onClick={handleProcessText}
              disabled={complaint.isProcessing}
            >
              {complaint.isProcessing
                ? "AI Processing..."
                : "Process Complaint with AI"}
            </button>

          </div>


          {/* MESSAGE */}
          {message && (
            <div className="ai-message">
              {message}
            </div>
          )}


          {/* AI RESULT */}
          <div className="ai-result">

            <h3>
              AI Copilot Risk Assessment
            </h3>


            {complaint.risk_level ? (

              <div className="risk-content">

                <div className="risk-item">

                  <strong>
                    Risk Level
                  </strong>

                  <span>
                    {complaint.risk_level}
                  </span>

                </div>


                {complaint.complaint_category && (
                  <div className="risk-item">

                    <strong>
                      Complaint Category
                    </strong>

                    <span>
                      {complaint.complaint_category}
                    </span>

                  </div>
                )}


                {complaint.severity && (
                  <div className="risk-item">

                    <strong>
                      Severity
                    </strong>

                    <span>
                      {complaint.severity}
                    </span>

                  </div>
                )}


                {complaint.risk_reason && (
                  <div className="risk-description">

                    <strong>
                      Assessment
                    </strong>

                    <p>
                      {complaint.risk_reason}
                    </p>

                  </div>
                )}


                {complaint.summary && (
                  <div className="risk-description">

                    <strong>
                      Complaint Summary
                    </strong>

                    <p>
                      {complaint.summary}
                    </p>

                  </div>
                )}


                {complaint.possible_duplicate && (
                  <div className="duplicate-warning">

                    <strong>
                      Possible Duplicate Complaint
                    </strong>

                    <p>
                      {complaint.duplicate_reason}
                    </p>

                    {complaint.duplicate_complaint_ids
                      ?.length > 0 && (
                      <p>
                        Existing complaint ID(s):{" "}
                        {complaint.duplicate_complaint_ids.join(
                          ", "
                        )}
                      </p>
                    )}

                  </div>
                )}

              </div>

            ) : (

              <div className="risk-placeholder">

                AI analysis will appear here after
                processing.

              </div>

            )}

          </div>

        </section>

      </main>
    </div>
  );
}

export default App;

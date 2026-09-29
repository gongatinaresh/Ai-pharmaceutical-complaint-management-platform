import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  status: "Pending Triage",

  // Complaint fields
  complaint_source: "",
  customer_name: "",

  product_name: "",
  product_strength_grade: "",
  batch_number: "",
  manufacturing_date: "",
  expiry_date: "",
  quantity_affected: "",

  complaint_type: "",
  complaint_date: "",
  detailed_description: "",

  initial_severity: "",
  priority: "",

  // AI results
  complaint_category: "",
  severity: "",
  risk_level: "",
  risk_reason: "",
  summary: "",

  // Duplicate detection
  possible_duplicate: false,
  duplicate_complaint_ids: [],
  duplicate_reason: "",

  // UI state
  isProcessing: false,
  error: null,
};

const complaintSlice = createSlice({
  name: "complaint",

  initialState,

  reducers: {
    // Update one form field
    updateField: (state, action) => {
      const { field, value } = action.payload;

      if (field in state) {
        state[field] = value;
      }
    },

    // Populate form fields from AI extraction
    populateFromAI: (state, action) => {
      const data = action.payload;

      Object.keys(data).forEach((field) => {
        if (
          field in state &&
          data[field] !== null &&
          data[field] !== undefined
        ) {
          state[field] = data[field];
        }
      });
    },

    // Store AI analysis results
    setAIResult: (state, action) => {
      const result = action.payload;

      state.complaint_category =
        result.complaint_category || "";

      state.severity =
        result.severity || "";

      state.risk_level =
        result.risk_level || "";

      state.risk_reason =
        result.risk_reason || "";

      state.summary =
        result.summary || "";

      // AI priority → form priority
      state.priority =
        result.priority || "";

      // AI severity → form initial severity
      state.initial_severity =
        result.severity ||
        state.initial_severity ||
        "";

      // Duplicate detection
      state.possible_duplicate =
        result.possible_duplicate || false;

      state.duplicate_complaint_ids =
        result.duplicate_complaint_ids || [];

      state.duplicate_reason =
        result.duplicate_reason || "";
    },

    // Loading state
    setProcessing: (state, action) => {
      state.isProcessing = action.payload;
    },

    // Error message
    setError: (state, action) => {
      state.error = action.payload;
    },

    // Reset everything
    resetComplaint: () => initialState,
  },
});

export const {
  updateField,
  populateFromAI,
  setAIResult,
  setProcessing,
  setError,
  resetComplaint,
} = complaintSlice.actions;

export default complaintSlice.reducer;
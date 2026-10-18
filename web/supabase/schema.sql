-- NICU-Math Supabase schema
-- Waveform data storage and NS analysis results

-- Patient context (de-identified per HIPAA/GDPR)
CREATE TABLE IF NOT EXISTS patients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  gestational_age_weeks NUMERIC(4,1) NOT NULL,
  birth_weight_grams INTEGER NOT NULL,
  postnatal_age_days INTEGER NOT NULL,
  surfactant_given BOOLEAN DEFAULT FALSE,
  surfactant_doses INTEGER DEFAULT 0,
  ventilator_mode TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT now(),
  notes TEXT DEFAULT ''
);

-- Waveform recording sessions
CREATE TABLE IF NOT EXISTS recordings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
  sample_rate_hz NUMERIC(6,1) NOT NULL DEFAULT 100.0,
  duration_seconds NUMERIC(10,2),
  n_samples INTEGER,
  fio2 NUMERIC(4,3) DEFAULT 0.21,
  peep NUMERIC(5,2) DEFAULT 5.0,
  source_type TEXT DEFAULT 'csv',
  uploaded_at TIMESTAMPTZ DEFAULT now(),
  meta JSONB DEFAULT '{}'
);

-- Individual breath cycles extracted from recordings
CREATE TABLE IF NOT EXISTS breath_cycles (
  id BIGSERIAL PRIMARY KEY,
  recording_id UUID NOT NULL REFERENCES recordings(id) ON DELETE CASCADE,
  breath_index INTEGER NOT NULL,
  start_sample INTEGER NOT NULL,
  end_sample INTEGER NOT NULL,
  dynamic_compliance NUMERIC(8,4),
  resistance NUMERIC(8,4),
  time_constant NUMERIC(8,6),
  work_of_breathing NUMERIC(10,4),
  pv_area NUMERIC(10,4),
  peak_pressure NUMERIC(6,2),
  tidal_volume NUMERIC(8,4),
  classification TEXT CHECK (classification IN ('smooth', 'approaching', 'critical', 'singular')),
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE (recording_id, breath_index)
);

-- Regularity analysis results (per recording window)
CREATE TABLE IF NOT EXISTS regularity_analyses (
  id BIGSERIAL PRIMARY KEY,
  recording_id UUID NOT NULL REFERENCES recordings(id) ON DELETE CASCADE,
  window_start INTEGER NOT NULL,
  window_end INTEGER NOT NULL,
  compliance_mean NUMERIC(8,4),
  compliance_trend NUMERIC(10,6),
  compliance_half_life NUMERIC(10,2),
  decay_exponent NUMERIC(8,4),
  t_star_estimate NUMERIC(10,2),
  lambda_param NUMERIC(12,4),
  re_max NUMERIC(8,2),
  pv_area_mean NUMERIC(10,4),
  enstrophy_mean NUMERIC(14,4),
  enstrophy_peak NUMERIC(14,4),
  classification TEXT CHECK (classification IN ('smooth', 'approaching', 'critical', 'singular')),
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Surfactant administration events detected or recorded
CREATE TABLE IF NOT EXISTS surfactant_events (
  id BIGSERIAL PRIMARY KEY,
  recording_id UUID NOT NULL REFERENCES recordings(id) ON DELETE CASCADE,
  breath_index INTEGER NOT NULL,
  event_type TEXT DEFAULT 'detected' CHECK (event_type IN ('detected', 'recorded')),
  compliance_before NUMERIC(8,4),
  compliance_after NUMERIC(8,4),
  improvement_ratio NUMERIC(6,4),
  classification_before TEXT,
  classification_after TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Critical constant estimates from clinical data
CREATE TABLE IF NOT EXISTS critical_constants (
  id BIGSERIAL PRIMARY KEY,
  lambda_star NUMERIC(14,4),
  compliance_threshold NUMERIC(8,4),
  gamma_critical NUMERIC(8,6),
  r_min_critical NUMERIC(12,10),
  confidence TEXT DEFAULT 'estimated',
  n_observations INTEGER,
  method TEXT DEFAULT 'midpoint',
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_breath_recording ON breath_cycles(recording_id);
CREATE INDEX IF NOT EXISTS idx_breath_classification ON breath_cycles(classification);
CREATE INDEX IF NOT EXISTS idx_analysis_recording ON regularity_analyses(recording_id);
CREATE INDEX IF NOT EXISTS idx_surfactant_recording ON surfactant_events(recording_id);
CREATE INDEX IF NOT EXISTS idx_recordings_patient ON recordings(patient_id);

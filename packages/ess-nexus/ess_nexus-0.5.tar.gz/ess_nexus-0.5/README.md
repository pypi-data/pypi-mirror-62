# ESS NEXUS PACKAGE

API for saving nexus style files at ESS for Accelerator division files.
Predifined format:


Fields red should be catalogued

    NXentry: timestamp for start and end of measurement/calibration, asset id, shift id
        run_cycle: (optional) NX_CHAR  correspond to the machine shift_id code
        entry_identifier: (mandatory) NX_CHAR correspond to the assed_id of a given equipment
        title: (optional) NX_CHAR
        experiment_description: (optional) NX_CHAR
        start_time: (mandatory) NX_DATE_TIME, for the calibration data it corresponds to the calibration date
        end_time:(optional) NX_DATE_TIME, for calibration data it corresponds to calibration due
        FileName: (mandatory) NX_CHAR, attribute necessary for the calibration database
        HDF5_Version: (mandatory) NX_CHAR, attribute necessary for the calibration database
        NeXus_Version: (mandatory) NX_CHAR, attribute necessary for the calibration database
        H5py_Version: (mandatory) NX_CHAR, attribute necessary for the calibration database
        NXuser
            name: (optional) NX_CHAR - Name of user responsible for this entry
            role: (optional) NX_CHAR  - Role of user responsible for this entry. Suggested roles are “local_contact”, “principal_investigator”, and “proposer”
            affiliation: (optional) NX_CHAR
            facility_user_id: (optional) NX_CHAR - inkind_id facility based unique identifier
        NXinstrument:
            Fields in blue are example of possible attibutes that can be added but won't be in the search
            NXradio_frequency:
                name: (optional) NX_CHAR
                location: (optional) NX_CHAR
                description: (optional) NX_CHAR
                type: (optional) NX_CHAR
                asset_id: (optional) NX_CHAR
                epics_channel[n]: (optional) NX_CHAR
                value[n]: (optional) NX_FLOAT {units=NX_ANY}
                forward_power[n]: (extra) NX_FLOAT {units=NX_POWER}
                reflected_power[n]: (extra)NX_FLOAT {units=NX_POWER}
                pulse_length[n]: (extra)NX_FLOAT {units=NX_PERIOD}
                repetition_rate[n]: (extra)NX_FLOAT {units=NX_FREQUENCY}
                amplitude[n]: (extra)NX_FLOAT {units=NX_VOLTAGE}
                phase[n]: (extra)NX_FLOAT {units=NX_ANGLE}
                temperature[n]: (extra)NX_FLOAT {units=NX_TEMPERATURE}
                duty_cycle[n]: (extra) NX_FLOAT {units=NX_ANY}
                etc.
            NXbeam_instrumentation:
                name: (optional) NX_CHAR
                location: (optional) NX_CHAR
                description: (optional) NX_CHAR
                type: (optional) NX_CHAR
                asset_id: (optional) NX_CHAR
                channel[n]: (optional) NX_CHAR
                epics_channels[n]: (optional) NX_CHAR
                value[n]: (optional) NX_FLOAT {units=NX_ANY}
                temperature[n]: (extra)NX_FLOAT {units=NX_TEMPERATURE}
                amplitude[n]: (extra)NX_FLOAT {units=NX_VOLTAGE}
                phase[n]: (extra)NX_FLOAT {units=NX_ANGLE}
                current[n]: (extra) NX_FLOAT {units=NX_CURRENT}
                etc.
            NXmagnet:
                name: (optional) NX_CHAR
                location: (optional) NX_CHAR
                description: (optional) NX_CHAR
                type: (optional) NX_CHAR
                asset _id: (optional) NX_CHAR
                epics_channel[n]: (optional) NX_CHAR
                value[n]: (optional) NX_FLOAT {units=NX_ANY}
                field[n]: (extra) NX_FLOAT {units=NX_ANY}
                set_current[n]: (extra) NX_FLOAT {units=NX_CURRENT}
                readback_current[n]: (extra) NX_FLOAT {units=NX_CURRENT}
                temperature[n]: (extra)NX_FLOAT {units=NX_TEMPERATURE}
                etc.
            NXlinac_element: (for any other equipment we might use like vaccum, gauges, timming etc..)
                name: (optional) NX_CHAR
                location: (optional) NX_CHAR
                description: (optional) NX_CHAR
                type: (optional) NX_CHAR
                asset_id: (optional) NX_CHAR
                epics_channel[n]: (optional) NX_CHAR
                value[n]: (optional) NX_FLOAT {units=NX_ANY}
                etc.
            NXlab_instrument: (equipment used in the lab for verification, calibration and etc and that will be not transferend to the linac later. Equipment used for measurement that don't belong to the linac and are used as support or for a short period of time as for example: spoces and network analyzers)
                name: (optional) NX_CHAR
                location: (optional) NX_CHAR
                description: (optional) NX_CHAR
                type: (optional) NX_CHAR
                asset_id: (optional) NX_CHAR
                epics_channel[n]: (optional) NX_CHAR
                channel[n]: (optional) NX_CHAR
                value[n]: (optional) NX_FLOAT {units=NX_ANY}
            NXsource (when dealing with beam)
                name: (optional) NX_CHAR
                type: (optional) NX_CHAR - Ion Source (for now fixed)
                probe: (optional) NX_CHAR - proton (fixed for now)
                power: (optional) NX_FLOAT {units=NX_POWER} - Final beam power
                emittance_x: (optional) NX_FLOAT {units=NX_EMITTANCE} - Source emittance (nm-rad) in X (horizontal) direction.
                emittance_y: (optional) NX_FLOAT {units=NX_EMITTANCE} - Source emittance (nm-rad) in Y (horizontal) direction.
                energy: (optional) NX_FLOAT {units=NX_ENERGY} - Beam final energy.
                current: (optional) NX_FLOAT {units=NX_CURRENT} - Total beam current per pulse
                frequency: (optional) NX_FLOAT {units=NX_FREQUENCY} - Source repetition rate
                pulse_width: (optional) NX_FLOAT {units=NX_TIME} - temporal width of source pulse
                mode: (optional) NX_CHAR -  type of beam (probe, slow tunning etc..) and destination
                notes: (optional) NXnote  - any source/facility related messages/events that occurred during the experiment
        Optional extra classes:
        NXdata
        NXLog
        NXNote
        NX Parameters
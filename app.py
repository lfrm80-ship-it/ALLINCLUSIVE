<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Wyndham All Inclusive - Support & Commercial Hub</title>
    
    <!-- LOGO / FAVICON PARA LA PESTAÑA DEL NAVEGADOR -->
    <link rel="icon" type="image/png" sizes="32x32" href="favicon.png">

    <!-- Chart.js para Gráficas -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <!-- Librerías para Exportación en Excel y PDF -->
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.28/jspdf.plugin.autotable.min.js"></script>

    <style>
        * { box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f6f9;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }

        /* SIDEBAR */
        .sidebar {
            width: 270px;
            background-color: #0b192c;
            color: white;
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
            border-right: 1px solid #1e293b;
        }

        .sidebar-header {
            padding: 25px 20px 15px 20px;
            background-color: #070f1e;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        
        .brand-logo-container {
            margin-bottom: 15px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .aimbridge-title {
            font-family: 'Georgia', serif;
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            letter-spacing: 0.5px;
            line-height: 1;
        }
        .aimbridge-sub {
            font-family: 'Segoe UI', sans-serif;
            font-size: 11px;
            font-weight: 700;
            color: #d1d5db;
            letter-spacing: 3.5px;
            margin-top: 4px;
            text-transform: uppercase;
        }

        .hub-title-divider {
            width: 80%;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            margin: 12px auto;
        }

        .sidebar-header h2 { 
            margin: 0; 
            font-size: 16px; 
            color: #38bdf8; 
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        .sidebar-header p { 
            margin: 4px 0 0 0; 
            font-size: 11px; 
            color: #94a3b8; 
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* SELECTOR DE IDIOMA EN SIDEBAR */
        .lang-switch-container {
            display: flex;
            justify-content: center;
            gap: 6px;
            margin-top: 12px;
        }
        .btn-lang {
            background-color: #1e293b;
            color: #94a3b8;
            border: 1px solid #334155;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn-lang:hover, .btn-lang.active {
            background-color: #0284c7;
            color: white;
            border-color: #38bdf8;
        }

        .sidebar-menu { list-style: none; padding: 0; margin: 15px 0; }
        .sidebar-menu li a {
            display: block;
            padding: 14px 20px;
            color: #94a3b8;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            border-left: 4px solid transparent;
            transition: all 0.25s ease;
        }
        .sidebar-menu li a:hover, 
        .sidebar-menu li a.active {
            background-color: #1e293b;
            color: #ffffff;
            border-left-color: #38bdf8;
        }

        /* AUTH / LOGIN BOX EN SIDEBAR */
        .user-auth-box {
            margin-top: auto;
            padding: 15px;
            background-color: #070f1e;
            border-top: 1px solid rgba(255,255,255,0.08);
            font-size: 12px;
        }
        .user-auth-box input {
            width: 100%;
            padding: 8px 10px;
            margin-bottom: 8px;
            border-radius: 4px;
            border: 1px solid #1e293b;
            background: #0b192c;
            color: #fff;
            font-size: 12px;
        }
        .btn-auth {
            width: 100%;
            padding: 8px;
            background-color: #0284c7;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            font-size: 12px;
            transition: background 0.2s;
        }
        .btn-auth:hover { background-color: #0369a1; }

        /* MAIN CONTENT */
        .main-content {
            flex-grow: 1;
            padding: 25px;
            overflow-y: auto;
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; }

        /* KPIS & CARDS */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .kpi-card {
            background: white;
            padding: 16px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            border-left: 5px solid #0b192c;
        }
        .kpi-card h4 { margin: 0; color: #64748b; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
        .kpi-card .number { font-size: 26px; font-weight: bold; margin: 6px 0 0 0; color: #0b192c; }

        .card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        .card-header-actions {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #f1f5f9;
            padding-bottom: 12px;
            margin-bottom: 15px;
        }
        .card-header-actions h3 { margin: 0; color: #0b192c; font-size: 17px; }

        /* FORMULARIO NUEVO TICKET */
        .editor-panel {
            display: none;
            background-color: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .editor-panel h4 { margin: 0 0 12px 0; color: #0b192c; font-size: 14px; }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-bottom: 10px;
        }
        .form-grid input, .form-grid select {
            padding: 8px;
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            font-size: 12px;
            width: 100%;
        }

        /* BOTONES DE ACCIÓN Y DESCARGA */
        .actions-group { display: flex; gap: 10px; }
        .btn-export {
            padding: 8px 14px;
            font-size: 12px;
            font-weight: 600;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
            text-decoration: none;
        }
        .btn-excel { background-color: #16a34a; color: white; }
        .btn-excel:hover { background-color: #15803d; }
        .btn-pdf { background-color: #dc2626; color: white; }
        .btn-pdf:hover { background-color: #b91c1c; }
        .btn-cloud { background-color: #0284c7; color: white; }
        .btn-cloud:hover { background-color: #0369a1; }
        .btn-edit-mode { background-color: #d97706; color: white; display: none; }
        .btn-add { background-color: #0284c7; color: white; border: none; padding: 8px 15px; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 12px; }

        /* TABLAS */
        table { width: 100%; border-collapse: collapse; font-size: 13px; }
        th, td { text-align: left; padding: 11px 12px; border-bottom: 1px solid #e2e8f0; }
        th { background-color: #f8fafc; color: #0b192c; font-weight: 700; }
        
        .badge { padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
        .badge-open { background-color: #fef2f2; color: #991b1b; }
        .badge-escalated { background-color: #f1f5f9; color: #334155; }
        .badge-closed { background-color: #f0fdf4; color: #166534; }

        .action-col { display: none; }
        .btn-delete { background-color: #ef4444; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 11px; }

        /* ESTILOS INTERACTIVOS DE WYNDHAM REWARDS (LEVELS & PERKS) */
        .tier-selector {
            display: flex;
            gap: 12px;
            margin-bottom: 25px;
        }
        .tier-card {
            flex: 1;
            padding: 16px;
            border-radius: 8px;
            background: white;
            border: 2px solid #e2e8f0;
            cursor: pointer;
            text-align: center;
            transition: all 0.25s ease;
        }
        .tier-card h4 { margin: 0; font-size: 16px; color: #0b192c; }
        .tier-card p { margin: 4px 0 0 0; font-size: 11px; color: #64748b; font-weight: 600; }
        
        .tier-card.blue.active { border-color: #0284c7; background: #f0f9ff; }
        .tier-card.gold.active { border-color: #d97706; background: #fffbeb; }
        .tier-card.platinum.active { border-color: #64748b; background: #f8fafc; }
        .tier-card.diamond.active { border-color: #0f172a; background: #f1f5f9; }

        .tier-card.blue.active h4 { color: #0284c7; }
        .tier-card.gold.active h4 { color: #d97706; }
        .tier-card.platinum.active h4 { color: #475569; }
        .tier-card.diamond.active h4 { color: #0f172a; }

        .perks-container {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 20px;
        }
        .tier-details-box {
            background: #ffffff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            border-top: 4px solid #0284c7;
        }
        .tier-details-box h3 { margin-top: 0; color: #0b192c; font-size: 18px; }
        .perk-list { list-style: none; padding: 0; margin: 15px 0 0 0; }
        .perk-list li {
            padding: 10px 0;
            border-bottom: 1px dashed #e2e8f0;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 13px;
            color: #334155;
        }
        .perk-list li:last-child { border-bottom: none; }
        .perk-icon { color: #16a34a; font-weight: bold; }

        .chart-box {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
    </style>
</head>
<body>

    <!-- MENÚ LATERAL -->
    <div class="sidebar">
        <div class="sidebar-header">
            <div class="brand-logo-container">
                <div class="aimbridge-title">Aimbridge</div>
                <div class="aimbridge-sub">LATAM</div>
            </div>
            
            <div class="hub-title-divider"></div>

            <h2>Wyndham All Inclusive</h2>
            <p id="txt-subhead">Panel Comercial & Soporte</p>

            <!-- SELECTOR DE IDIOMA -->
            <div class="lang-switch-container">
                <button class="btn-lang active" id="btn-es" onclick="switchLanguage('es')">ESP</button>
                <button class="btn-lang" id="btn-en" onclick="switchLanguage('en')">ENG</button>
            </div>
        </div>

        <ul class="sidebar-menu">
            <li><a href="#" id="menu-tickets" class="active" onclick="switchTab(event, 'tickets')">Wyndham Tickets</a></li>
            <li><a href="#" id="menu-promos" onclick="switchTab(event, 'promociones')">Promociones</a></li>
            <li><a href="#" id="menu-rewards" onclick="switchTab(event, 'rewards')">Wyndham Rewards</a></li>
            <li><a href="#" id="menu-formatos" onclick="switchTab(event, 'formatos')">Formatos y Consultas</a></li>
        </ul>

        <!-- USUARIO / LOGIN -->
        <div class="user-auth-box">
            <div id="login-form">
                <p id="txt-login-header" style="margin: 0 0 8px 0; font-weight: bold; color: #cbd5e1;">Acceso Editor</p>
                <input type="text" id="username" placeholder="Usuario">
                <input type="password" id="password" placeholder="Contraseña">
                <button class="btn-auth" id="btn-login" onclick="handleLogin()">Ingresar</button>
            </div>
            <div id="user-logged" style="display: none;">
                <p id="txt-logged-label" style="margin: 0 0 4px 0; color: #94a3b8;">Sesión activa:</p>
                <p style="margin: 0 0 10px 0; font-weight: bold; color: #38bdf8;" id="logged-user-name">Admin</p>
                <button class="btn-auth" id="btn-logout" style="background-color: #ef4444;" onclick="handleLogout()">Cerrar Sesión</button>
            </div>
        </div>
    </div>

    <!-- CONTENIDO PRINCIPAL -->
    <div class="main-content">

        <!-- SECCIÓN 1: WYNDHAM TICKETS -->
        <div id="tickets" class="tab-content active">
            <h2 id="txt-tickets-main-title">Módulo de Tickets de Soporte Wyndham</h2>
            
            <div class="kpi-grid">
                <div class="kpi-card">
                    <h4 id="lbl-kpi-total">Total Tickets</h4>
                    <div class="number" id="kpi-total">28</div>
                </div>
                <div class="kpi-card" style="border-left-color: #ef4444;">
                    <h4 id="lbl-kpi-open">Abiertos (Open)</h4>
                    <div class="number" id="kpi-open">4</div>
                </div>
                <div class="kpi-card" style="border-left-color: #475569;">
                    <h4 id="lbl-kpi-escalated">Escalados</h4>
                    <div class="number" id="kpi-escalated">4</div>
                </div>
                <div class="kpi-card" style="border-left-color: #22c55e;">
                    <h4 id="lbl-kpi-closed">Cerrados</h4>
                    <div class="number" id="kpi-closed">20</div>
                </div>
            </div>

            <!-- PANEL DE ALTA DE NUEVO TICKET -->
            <div id="add-ticket-panel" class="editor-panel">
                <h4 id="txt-add-ticket-title">➕ Registrar Nuevo Ticket</h4>
                <div class="form-grid">
                    <select id="new-status">
                        <option value="Open">Open</option>
                        <option value="Escalated">Escalated</option>
                        <option value="Closed">Closed</option>
                    </select>
                    <input type="text" id="new-ticket" placeholder="Ej. #12220000">
                    <select id="new-prop">
                        <option value="WYPC">WYPC</option>
                        <option value="WYSAM">WYSAM</option>
                        <option value="WYPC - WYSAM">WYPC - WYSAM</option>
                    </select>
                    <input type="text" id="new-partner" placeholder="Partner / Área">
                    <input type="text" id="new-date" placeholder="DD/MM/AAAA">
                    <input type="text" id="new-details" placeholder="Siguiente Paso / Detalle">
                </div>
                <button class="btn-add" id="btn-save-ticket" onclick="addNewTicket()">Guardar Ticket</button>
            </div>

            <div class="card">
                <div class="card-header-actions">
                    <h3 id="txt-table-title">Bitácora de Conectividad & Soporte</h3>
                    <div class="actions-group">
                        <button class="btn-export btn-excel" id="btn-export-excel" onclick="exportToExcel()">📊 Exportar Excel</button>
                        <button class="btn-export btn-pdf" id="btn-export-pdf" onclick="exportToPDF()">📄 Exportar PDF</button>
                        <button id="btn-edit-action" class="btn-export btn-edit-mode" onclick="enableEditMode()">✏️ Activar Edición Directa</button>
                    </div>
                </div>

                <table id="ticketsTable">
                    <thead>
                        <tr>
                            <th id="th-status">Estatus</th>
                            <th id="th-ticket">Ticket #</th>
                            <th id="th-prop">Propiedad</th>
                            <th id="th-partner">Partner / Área</th>
                            <th id="th-date">Fecha Apertura</th>
                            <th id="th-details">Siguiente Paso / Detalles</th>
                            <th class="action-col" id="th-action">Acción</th>
                        </tr>
                    </thead>
                    <tbody id="tickets-tbody">
                        <tr>
                            <td><span class="badge badge-open">Open</span></td>
                            <td><b>#12214999</b></td>
                            <td>WYPC</td>
                            <td>RFP - Rate plan loading form</td>
                            <td>13/09/2026</td>
                            <td>Revisión de carga de tarifario RFP</td>
                            <td class="action-col"><button class="btn-delete" onclick="deleteRow(this)">Eliminar</button></td>
                        </tr>
                        <tr>
                            <td><span class="badge badge-open">Open</span></td>
                            <td><b>#12207447</b></td>
                            <td>WYSAM</td>
                            <td>Expedia AO Names</td>
                            <td>09/11/2026</td>
                            <td>Validación nombres AO Expedia Samaná</td>
                            <td class="action-col"><button class="btn-delete" onclick="deleteRow(this)">Eliminar</button></td>
                        </tr>
                        <tr>
                            <td><span class="badge badge-open">Open</span></td>
                            <td><b>#12207368</b></td>
                            <td>WYPC</td>
                            <td>Expedia AO Names</td>
                            <td>09/11/2026</td>
                            <td>Validación nombres AO Expedia Punta Cana</td>
                            <td class="action-col"><button class="btn-delete" onclick="deleteRow(this)">Eliminar</button></td>
                        </tr>
                        <tr>
                            <td><span class="badge badge-open">Open</span></td>
                            <td><b>#12037051</b></td>
                            <td>WYPC - WYSAM</td>
                            <td>House - Reservations issue</td>
                            <td>11/08/2026</td>
                            <td>Investigación reservas sin referencia externa</td>
                            <td class="action-col"><button class="btn-delete" onclick="deleteRow(this)">Eliminar</button></td>
                        </tr>
                        <tr>
                            <td><span class="badge badge-escalated">Escalated</span></td>
                            <td><b>#11898107</b></td>
                            <td>WYPC - WYSAM</td>
                            <td>Transat-Air Canada - Company Profile</td>
                            <td>19/07/2026</td>
                            <td>Falta External Reference en SynXis / Opera</td>
                            <td class="action-col"><button class="btn-delete" onclick="deleteRow(this)">Eliminar</button></td>
                        </tr>
                        <tr>
                            <td><span class="badge badge-escalated">Escalated</span></td>
                            <td><b>#11925162</b></td>
                            <td>WYPC - WYSAM</td>
                            <td>House Level - Profile</td>
                            <td>23/07/2026</td>
                            <td>Creación de Company Profiles en SynXis</td>
                            <td class="action-col"><button class="btn-delete" onclick="deleteRow(this)">Eliminar</button></td>
                        </tr>
                        <tr>
                            <td><span class="badge badge-closed">Closed</span></td>
                            <td><b>#12088979</b></td>
                            <td>WYPC</td>
                            <td>AO - Section</td>
                            <td>19/08/2026</td>
                            <td>Completado Wyn</td>
                            <td class="action-col"><button class="btn-delete" onclick="deleteRow(this)">Eliminar</button></td>
                        </tr>
                        <tr>
                            <td><span class="badge badge-closed">Closed</span></td>
                            <td><b>#12088918</b></td>
                            <td>WYSAM</td>
                            <td>AO - Section</td>
                            <td>19/08/2026</td>
                            <td>Completado Wyn</td>
                            <td class="action-col"><button class="btn-delete" onclick="deleteRow(this)">Eliminar</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- SECCIÓN 2: PROMOCIONES -->
        <div id="promociones" class="tab-content">
            <h2 id="txt-promos-title">Módulo de Promociones</h2>
            <div class="card"><p id="txt-promos-body">Contenido de promociones...</p></div>
        </div>

        <!-- SECCIÓN 3: WYNDHAM REWARDS INTERACTIVO -->
        <div id="rewards" class="tab-content">
            <h2 id="txt-rewards-title">Wyndham Rewards - Member Levels & Benefits</h2>
            <p id="txt-rewards-desc" style="color: #64748b; font-size: 13px; margin-top: -8px; margin-bottom: 20px;">
                Explora las ventajas por nivel de membresía y el rendimiento comercial de la cartera de miembros Wyndham Rewards.
            </p>

            <div class="tier-selector">
                <div class="tier-card blue active" onclick="selectTier('blue', this)">
                    <h4>BLUE</h4>
                    <p id="sub-blue">0 Noches / Registro</p>
                </div>
                <div class="tier-card gold" onclick="selectTier('gold', this)">
                    <h4>GOLD</h4>
                    <p id="sub-gold">5 Noches Cualificadas</p>
                </div>
                <div class="tier-card platinum" onclick="selectTier('platinum', this)">
                    <h4>PLATINUM</h4>
                    <p id="sub-plat">15 Noches Cualificadas</p>
                </div>
                <div class="tier-card diamond" onclick="selectTier('diamond', this)">
                    <h4>DIAMOND</h4>
                    <p id="sub-diam">40 Noches Cualificadas</p>
                </div>
            </div>

            <div class="perks-container">
                <div class="tier-details-box" id="tier-info-box">
                    <h3 id="tier-title" style="color: #0284c7;">Nivel BLUE - Beneficios Básicos</h3>
                    <ul class="perk-list" id="tier-perks-list">
                        <li><span class="perk-icon">✓</span> 10 puntos por dólar o 1,000 puntos en estadías calificados</li>
                        <li><span class="perk-icon">✓</span> Wi-Fi gratuito en todas las propiedades All Inclusive</li>
                        <li><span class="perk-icon">✓</span> Rollover Nights (Noches acumulables para el siguiente año)</li>
                    </ul>
                </div>

                <div class="chart-box">
                    <h3 id="txt-chart-title" style="margin-top:0; font-size:15px; color:#0b192c;">Penetración de Reservas por Nivel de Socio</h3>
                    <canvas id="rewardsChart" height="130"></canvas>
                </div>
            </div>
        </div>

        <!-- SECCIÓN 4: FORMATOS Y CONSULTAS -->
        <div id="formatos" class="tab-content">
            <h2 id="txt-formatos-title">Centro de Formatos & Descargas</h2>
            <p id="txt-formatos-desc" style="color: #64748b; font-size: 13px; margin-top: -8px; margin-bottom: 20px;">
                Descarga plantillas operativas, formatos de auditoría y documentos de consulta directa.
            </p>

            <div class="kpi-grid">
                <!-- Tarjeta 1: Archivo de prueba -->
                <div class="card" style="margin-bottom: 0;">
                    <h3 id="txt-fmt-test-title" style="font-size: 15px; color: #0b192c; margin-top: 0;">📊 Matriz Comercial & Test</h3>
                    <p id="txt-fmt-test-desc" style="font-size: 12px; color: #64748b;">Plantilla en Excel para pruebas de auditoría y carga de tarifas.</p>
                    <a href="formatos/test.xlsx" download="Matriz_Test_Comercial.xlsx" class="btn-export btn-excel" style="width: 100%; justify-content: center; margin-top: 10px;">
                        📥 Descargar Excel (test.xlsx)
                    </a>
                </div>

                <!-- Tarjeta 2: PDF -->
                <div class="card" style="margin-bottom: 0;">
                    <h3 id="txt-fmt-pdf-title" style="font-size: 15px; color: #0b192c; margin-top: 0;">📋 Check-list de Paridad</h3>
                    <p id="txt-fmt-pdf-desc" style="font-size: 12px; color: #64748b;">Formato PDF para reporte de disparidades en OTAs.</p>
                    <a href="formatos/checklist_paridad.pdf" download="Checklist_Paridad.pdf" class="btn-export btn-pdf" style="width: 100%; justify-content: center; margin-top: 10px;">
                        📄 Descargar PDF
                    </a>
                </div>

                <!-- Tarjeta 3: Enlace a Nube -->
                <div class="card" style="margin-bottom: 0;">
                    <h3 id="txt-fmt-cloud-title" style="font-size: 15px; color: #0b192c; margin-top: 0;">☁️ Manuales en la Nube</h3>
                    <p id="txt-fmt-cloud-desc" style="font-size: 12px; color: #64748b;">Acceso directo al directorio de documentos compartidos.</p>
                    <a href="https://drive.google.com" target="_blank" class="btn-export btn-cloud" style="width: 100%; justify-content: center; margin-top: 10px;">
                        🔗 Abrir Carpeta
                    </a>
                </div>
            </div>
        </div>

    </div>

    <!-- JAVASCRIPT: LÓGICA GENERAL, TRADUCCIONES & REWARDS -->
    <script>
        const CREDS = { user: "admin", pass: "wyndham2026" };
        let currentLang = 'es';
        let currentSelectedTier = 'blue';

        // DICCIONARIO DE IDIOMAS
        const i18n = {
            es: {
                subhead: "Panel Comercial & Soporte",
                menuTickets: "Wyndham Tickets",
                menuPromos: "Promociones",
                menuRewards: "Wyndham Rewards",
                menuFormatos: "Formatos y Consultas",
                loginHeader: "Acceso Editor",
                btnLogin: "Ingresar",
                loggedLabel: "Sesión activa:",
                btnLogout: "Cerrar Sesión",
                ticketsMainTitle: "Módulo de Tickets de Soporte Wyndham",
                kpiTotal: "Total Tickets",
                kpiOpen: "Abiertos (Open)",
                kpiEscalated: "Escalados",
                kpiClosed: "Cerrados",
                addTicketTitle: "➕ Registrar Nuevo Ticket",
                btnSaveTicket: "Guardar Ticket",
                tableTitle: "Bitácora de Conectividad & Soporte",
                btnExcel: "📊 Exportar Excel",
                btnPdf: "📄 Exportar PDF",
                btnEdit: "✏️ Activar Edición Directa",
                thStatus: "Estatus",
                thTicket: "Ticket #",
                thProp: "Propiedad",
                thPartner: "Partner / Área",
                thDate: "Fecha Apertura",
                thDetails: "Siguiente Paso / Detalles",
                thAction: "Acción",
                promosTitle: "Módulo de Promociones",
                promosBody: "Contenido de promociones...",
                rewardsTitle: "Wyndham Rewards - Member Levels & Benefits",
                rewardsDesc: "Explora las ventajas por nivel de membresía y el rendimiento comercial de la cartera de miembros Wyndham Rewards.",
                subBlue: "0 Noches / Registro",
                subGold: "5 Noches Cualificadas",
                subPlat: "15 Noches Cualificadas",
                subDiam: "40 Noches Cualificadas",
                chartTitle: "Penetración de Reservas por Nivel de Socio",
                chartLabel: "% Share de Reservas en Resorts All Inclusive",
                formatosTitle: "Centro de Formatos & Descargas",
                formatosDesc: "Descarga plantillas operativas, formatos de auditoría y documentos de consulta directa.",
                fmtTestTitle: "📊 Matriz Comercial & Test",
                fmtTestDesc: "Plantilla en Excel para pruebas de auditoría y carga de tarifas.",
                fmtPdfTitle: "📋 Check-list de Paridad",
                fmtPdfDesc: "Formato PDF para reporte de disparidades en OTAs.",
                fmtCloudTitle: "☁️ Manuales en la Nube",
                fmtCloudDesc: "Acceso directo al directorio de documentos compartidos.",
                btnDelete: "Eliminar",
                phTicket: "Ej. #12220000",
                phPartner: "Partner / Área",
                phDate: "DD/MM/AAAA",
                phDetails: "Siguiente Paso / Detalle",
                phUser: "Usuario",
                phPass: "Contraseña"
            },
            en: {
                subhead: "Commercial & Support Hub",
                menuTickets: "Wyndham Tickets",
                menuPromos: "Promotions",
                menuRewards: "Wyndham Rewards",
                menuFormatos: "Forms & Downloads",
                loginHeader: "Editor Access",
                btnLogin: "Log In",
                loggedLabel: "Active session:",
                btnLogout: "Log Out",
                ticketsMainTitle: "Wyndham Support Tickets Module",
                kpiTotal: "Total Tickets",
                kpiOpen: "Open Tickets",
                kpiEscalated: "Escalated",
                kpiClosed: "Closed",
                addTicketTitle: "➕ Add New Ticket",
                btnSaveTicket: "Save Ticket",
                tableTitle: "Connectivity & Support Log",
                btnExcel: "📊 Export Excel",
                btnPdf: "📄 Export PDF",
                btnEdit: "✏️ Enable Direct Edit",
                thStatus: "Status",
                thTicket: "Ticket #",
                thProp: "Property",
                thPartner: "Partner / Area",
                thDate: "Opening Date",
                thDetails: "Next Step / Details",
                thAction: "Action",
                promosTitle: "Promotions Module",
                promosBody: "Promotions content...",
                rewardsTitle: "Wyndham Rewards - Member Levels & Benefits",
                rewardsDesc: "Explore benefits by membership level and commercial performance of the Wyndham Rewards member base.",
                subBlue: "0 Nights / Sign Up",
                subGold: "5 Qualified Nights",
                subPlat: "15 Qualified Nights",
                subDiam: "40 Qualified Nights",
                chartTitle: "Booking Penetration by Member Tier",
                chartLabel: "% Share of Bookings in All Inclusive Resorts",
                formatosTitle: "Forms & Reference Center",
                formatosDesc: "Download operational templates, audit forms, and direct reference documents.",
                fmtTestTitle: "📊 Commercial & Test Matrix",
                fmtTestDesc: "Excel template for rate auditing and rate plan testing.",
                fmtPdfTitle: "📋 Parity Check-list",
                fmtPdfDesc: "PDF form for reporting OTA disparities.",
                fmtCloudTitle: "☁️ Cloud Manuals",
                fmtCloudDesc: "Direct link to shared document drive.",
                btnDelete: "Delete",
                phTicket: "Ex. #12220000",
                phPartner: "Partner / Area",
                phDate: "DD/MM/YYYY",
                phDetails: "Next Step / Detail",
                phUser: "Username",
                phPass: "Password"
            }
        };

        const tierData = {
            blue: {
                color: "#0284c7",
                title: { es: "Nivel BLUE - Beneficios Básicos", en: "BLUE Level - Basic Perks" },
                perks: {
                    es: [
                        "10 puntos por cada $1 USD gastado (o 1,000 puntos mínimo)",
                        "Wi-Fi de alta velocidad gratuito",
                        "Rollover Nights (Noches acumulables)",
                        "Tarifa exclusiva para miembros en canal directo"
                    ],
                    en: [
                        "10 points per $1 USD spent (or 1,000 minimum points)",
                        "Free High-Speed Wi-Fi",
                        "Rollover Nights (Roll over unused nights)",
                        "Exclusive Member Rate on direct channel"
                    ]
                }
            },
            gold: {
                color: "#d97706",
                title: { es: "Nivel GOLD - Noches Preferentes & Upgrades", en: "GOLD Level - Preferred Room & Upgrades" },
                perks: {
                    es: [
                        "Todos los beneficios del Nivel Blue",
                        "10% de bonus sobre puntos base ganados",
                        "Elección de habitación preferida dentro de la categoría",
                        "Late Check-out (Sujeto a disponibilidad)",
                        "Descuentos en amenities en propiedades resort seleccionadas"
                    ],
                    en: [
                        "All Blue Level benefits",
                        "10% bonus points on base points",
                        "Preferred room choice within category",
                        "Late Check-out (Subject to availability)",
                        "Discounts on amenities at select resort properties"
                    ]
                }
            },
            platinum: {
                color: "#475569",
                title: { es: "Nivel PLATINUM - Experiencia VIP Superior", en: "PLATINUM Level - Superior VIP Experience" },
                perks: {
                    es: [
                        "Todos los beneficios del Nivel Gold",
                        "15% de bonus sobre puntos base ganados",
                        "Early Check-in prioritario",
                        "Upgrade de habitación a categoría superior (sujeto a disponibilidad)",
                        "Acelerador de puntos en promociones exclusivas"
                    ],
                    en: [
                        "All Gold Level benefits",
                        "15% bonus points on base points",
                        "Priority Early Check-in",
                        "Room upgrade to preferred category (subject to availability)",
                        "Point accelerator on exclusive promotions"
                    ]
                }
            },
            diamond: {
                color: "#0f172a",
                title: { es: "Nivel DIAMOND - Elite All Inclusive Benefits", en: "DIAMOND Level - Elite All Inclusive Perks" },
                perks: {
                    es: [
                        "Todos los beneficios del Nivel Platinum",
                        "20% de bonus sobre puntos base ganados",
                        "Upgrade a Suite garantizado según disponibilidad",
                        "Regalo de bienvenida personalizado al check-in (Fruit/Wine Basket)",
                        "Posibilidad de regalar membresía Gold a un familiar o amigo",
                        "Atención telefónica de concierge dedicada 24/7"
                    ],
                    en: [
                        "All Platinum Level benefits",
                        "20% bonus points on base points",
                        "Suite upgrade according to availability",
                        "Personalized welcome amenity upon arrival",
                        "Ability to gift a Gold Membership to a family member or friend",
                        "24/7 Dedicated Concierge Support"
                    ]
                }
            }
        };

        // FUNCIÓN CAMBIO DE IDIOMA
        function switchLanguage(lang) {
            currentLang = lang;
            document.getElementById('btn-es').classList.toggle('active', lang === 'es');
            document.getElementById('btn-en').classList.toggle('active', lang === 'en');

            const t = i18n[lang];

            // Textos generales
            document.getElementById('txt-subhead').innerText = t.subhead;
            document.getElementById('menu-tickets').innerText = t.menuTickets;
            document.getElementById('menu-promos').innerText = t.menuPromos;
            document.getElementById('menu-rewards').innerText = t.menuRewards;
            document.getElementById('menu-formatos').innerText = t.menuFormatos;
            document.getElementById('txt-login-header').innerText = t.loginHeader;
            document.getElementById('btn-login').innerText = t.btnLogin;
            document.getElementById('txt-logged-label').innerText = t.loggedLabel;
            document.getElementById('btn-logout').innerText = t.btnLogout;
            
            document.getElementById('username').placeholder = t.phUser;
            document.getElementById('password').placeholder = t.phPass;

            // Seccion Tickets
            document.getElementById('txt-tickets-main-title').innerText = t.ticketsMainTitle;
            document.getElementById('lbl-kpi-total').innerText = t.kpiTotal;
            document.getElementById('lbl-kpi-open').innerText = t.kpiOpen;
            document.getElementById('lbl-kpi-escalated').innerText = t.kpiEscalated;
            document.getElementById('lbl-kpi-closed').innerText = t.kpiClosed;
            document.getElementById('txt-add-ticket-title').innerText = t.addTicketTitle;
            document.getElementById('btn-save-ticket').innerText = t.btnSaveTicket;
            document.getElementById('txt-table-title').innerText = t.tableTitle;
            document.getElementById('btn-export-excel').innerText = t.btnExcel;
            document.getElementById('btn-export-pdf').innerText = t.btnPdf;
            document.getElementById('btn-edit-action').innerText = t.btnEdit;

            document.getElementById('new-ticket').placeholder = t.phTicket;
            document.getElementById('new-partner').placeholder = t.phPartner;
            document.getElementById('new-date').placeholder = t.phDate;
            document.getElementById('new-details').placeholder = t.phDetails;

            document.getElementById('th-status').innerText = t.thStatus;
            document.getElementById('th-ticket').innerText = t.thTicket;
            document.getElementById('th-prop').innerText = t.thProp;
            document.getElementById('th-partner').innerText = t.thPartner;
            document.getElementById('th-date').innerText = t.thDate;
            document.getElementById('th-details').innerText = t.thDetails;
            document.getElementById('th-action').innerText = t.thAction;

            document.querySelectorAll('.btn-delete').forEach(b => b.innerText = t.btnDelete);

            // Seccion Promos
            document.getElementById('txt-promos-title').innerText = t.promosTitle;
            document.getElementById('txt-promos-body').innerText = t.promosBody;

            // Seccion Rewards
            document.getElementById('txt-rewards-title').innerText = t.rewardsTitle;
            document.getElementById('txt-rewards-desc').innerText = t.rewardsDesc;
            document.getElementById('sub-blue').innerText = t.subBlue;
            document.getElementById('sub-gold').innerText = t.subGold;
            document.getElementById('sub-plat').innerText = t.subPlat;
            document.getElementById('sub-diam').innerText = t.subDiam;
            document.getElementById('txt-chart-title').innerText = t.chartTitle;

            // Seccion Formatos
            document.getElementById('txt-formatos-title').innerText = t.formatosTitle;
            document.getElementById('txt-formatos-desc').innerText = t.formatosDesc;
            document.getElementById('txt-fmt-test-title').innerText = t.fmtTestTitle;
            document.getElementById('txt-fmt-test-desc').innerText = t.fmtTestDesc;
            document.getElementById('txt-fmt-pdf-title').innerText = t.fmtPdfTitle;
            document.getElementById('txt-fmt-pdf-desc').innerText = t.fmtPdfDesc;
            document.getElementById('txt-fmt-cloud-title').innerText = t.fmtCloudTitle;
            document.getElementById('txt-fmt-cloud-desc').innerText = t.fmtCloudDesc;

            updateTierUI(currentSelectedTier);

            if (chartInstance) {
                chartInstance.data.datasets[0].label = t.chartLabel;
                chartInstance.update();
            }
        }

        function switchTab(event, tabId) {
            event.preventDefault();
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.sidebar-menu a').forEach(l => l.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');

            if (tabId === 'rewards') {
                initRewardsChart();
            }
        }

        function selectTier(tierKey, cardEl) {
            document.querySelectorAll('.tier-card').forEach(c => c.classList.remove('active'));
            if (cardEl) cardEl.classList.add('active');
            currentSelectedTier = tierKey;
            updateTierUI(tierKey);
        }

        function updateTierUI(tierKey) {
            const data = tierData[tierKey];
            const box = document.getElementById('tier-info-box');
            const title = document.getElementById('tier-title');
            const list = document.getElementById('tier-perks-list');

            box.style.borderTopColor = data.color;
            title.innerText = data.title[currentLang];
            title.style.color = data.color;

            list.innerHTML = data.perks[currentLang].map(p => `<li><span class="perk-icon">✓</span> ${p}</li>`).join('');
        }

        let chartInstance = null;
        function initRewardsChart() {
            if (chartInstance) return;
            const ctx = document.getElementById('rewardsChart').getContext('2d');
            chartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Blue', 'Gold', 'Platinum', 'Diamond'],
                    datasets: [{
                        label: i18n[currentLang].chartLabel,
                        data: [45, 30, 15, 10],
                        backgroundColor: ['#0284c7', '#d97706', '#64748b', '#0f172a'],
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true, max: 50 } }
                }
            });
        }

        function handleLogin() {
            const usr = document.getElementById('username').value.trim();
            const pwd = document.getElementById('password').value.trim();

            if (usr === CREDS.user && pwd === CREDS.pass) {
                document.getElementById('login-form').style.display = 'none';
                document.getElementById('user-logged').style.display = 'block';
                document.getElementById('logged-user-name').innerText = usr;
                document.getElementById('btn-edit-action').style.display = 'inline-flex';
                document.getElementById('add-ticket-panel').style.display = 'block';
                enableEditMode();
                alert(currentLang === 'es' ? '¡Autenticación exitosa! Modo Editor habilitado.' : 'Authentication successful! Editor Mode enabled.');
            } else {
                alert(currentLang === 'es' ? 'Usuario o contraseña incorrectos.' : 'Invalid username or password.');
            }
        }

        function handleLogout() {
            document.getElementById('login-form').style.display = 'block';
            document.getElementById('user-logged').style.display = 'none';
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
            document.getElementById('btn-edit-action').style.display = 'none';
            document.getElementById('add-ticket-panel').style.display = 'none';

            document.querySelectorAll('#ticketsTable td').forEach(td => td.contentEditable = "false");
            document.querySelectorAll('.action-col').forEach(col => col.style.display = 'none');
        }

        function enableEditMode() {
            document.querySelectorAll('#ticketsTable td:not(.action-col)').forEach(td => {
                td.contentEditable = "true";
                td.style.backgroundColor = "#fffbeb";
            });
            document.querySelectorAll('.action-col').forEach(col => col.style.display = 'table-cell');
        }

        function addNewTicket() {
            const status = document.getElementById('new-status').value;
            const ticket = document.getElementById('new-ticket').value.trim();
            const prop = document.getElementById('new-prop').value;
            const partner = document.getElementById('new-partner').value.trim();
            const date = document.getElementById('new-date').value.trim();
            const details = document.getElementById('new-details').value.trim();

            if (!ticket) {
                alert(currentLang === 'es' ? 'Por favor ingresa el número de ticket.' : 'Please enter ticket number.');
                return;
            }

            let badgeClass = 'badge-open';
            if (status === 'Escalated') badgeClass = 'badge-escalated';
            if (status === 'Closed') badgeClass = 'badge-closed';

            const tbody = document.getElementById('tickets-tbody');
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
                <td contenteditable="true" style="background-color: #fffbeb;"><span class="badge ${badgeClass}">${status}</span></td>
                <td contenteditable="true" style="background-color: #fffbeb;"><b>${ticket}</b></td>
                <td contenteditable="true" style="background-color: #fffbeb;">${prop}</td>
                <td contenteditable="true" style="background-color: #fffbeb;">${partner}</td>
                <td contenteditable="true" style="background-color: #fffbeb;">${date}</td>
                <td contenteditable="true" style="background-color: #fffbeb;">${details}</td>
                <td class="action-col" style="display: table-cell;"><button class="btn-delete" onclick="deleteRow(this)">${i18n[currentLang].btnDelete}</button></td>
            `;
            tbody.prepend(newRow);

            document.getElementById('new-ticket').value = '';
            document.getElementById('new-partner').value = '';
            document.getElementById('new-date').value = '';
            document.getElementById('new-details').value = '';
        }

        function deleteRow(btn) {
            const confirmMsg = currentLang === 'es' ? '¿Deseas eliminar este registro?' : 'Do you want to delete this record?';
            if (confirm(confirmMsg)) {
                btn.closest('tr').remove();
            }
        }

        function exportToExcel() {
            const table = document.getElementById("ticketsTable");
            const wb = XLSX.utils.table_to_book(table, { sheet: "Tickets Wyndham" });
            XLSX.writeFile(wb, "Wyndham_All_Inclusive_Tickets.xlsx");
        }

        function exportToPDF() {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF('landscape');

            doc.setFontSize(16);
            doc.setTextColor(11, 25, 44);
            doc.text("Aimbridge LATAM - Wyndham All Inclusive", 14, 15);
            doc.setFontSize(11);
            doc.setTextColor(100);
            doc.text(`Reporte de Soporte & Conectividad | Exportado: ${new Date().toLocaleDateString()}`, 14, 22);

            doc.autoTable({
                html: '#ticketsTable',
                startY: 28,
                theme: 'grid',
                headStyles: { fillColor: [11, 25, 44], textColor: [255, 255, 255] },
                styles: { fontSize: 9, cellPadding: 3 }
            });

            doc.save("Wyndham_All_Inclusive_Tickets.pdf");
        }
    </script>
</body>
</html>

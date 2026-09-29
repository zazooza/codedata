const $ = (selector) => document.querySelector(selector);
const labels = { class_name: "ชื่อคลาส", booking_count: "จำนวนการจอง", status: "สถานะ" };

async function api(url) {
  const response = await fetch(url);
  const result = await response.json();
  if (!response.ok || !result.ok) throw new Error(result.error || "โหลดรายงานไม่สำเร็จ");
  return result.data;
}

function renderTable(selector, rows) {
  const table = $(selector);
  const head = table.querySelector("thead");
  const body = table.querySelector("tbody");
  head.replaceChildren();
  body.replaceChildren();
  if (!rows.length) return;
  const columns = Object.keys(rows[0]);
  const headerRow = document.createElement("tr");
  for (const column of columns) {
    const th = document.createElement("th");
    th.textContent = labels[column] || column;
    headerRow.append(th);
  }
  head.append(headerRow);
  for (const row of rows) {
    const tr = document.createElement("tr");
    for (const column of columns) {
      const td = document.createElement("td");
      td.textContent = row[column] ?? "—";
      tr.append(td);
    }
    body.append(tr);
  }
}

async function loadReports() {
  try {
    const summary = await api("/api/reports/summary");
    const summaryLabels = {
      members: "สมาชิก", trainers: "เทรนเนอร์", classes: "คลาส",
      bookings: "การจอง", equipment: "อุปกรณ์"
    };
    const cards = Object.entries(summaryLabels).map(([key, label]) => {
      const card = document.createElement("div");
      card.className = "metric";
      const number = document.createElement("div");
      number.className = "metric-num";
      number.textContent = summary[key] ?? 0;
      const caption = document.createElement("div");
      caption.className = "metric-label";
      caption.textContent = label;
      card.append(number, caption);
      return card;
    });
    $("#summary").replaceChildren(...cards);
    renderTable("#popularTable", await api("/api/reports/popular-classes"));
    renderTable("#statusTable", await api("/api/reports/booking-status"));
  } catch (error) {
    $("#popularStatus").textContent = error.message;
    $("#popularStatus").className = "status err";
  }
}

loadReports();

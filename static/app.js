const ENTITIES = {
  members: {
    label: "สมาชิก", api: "/api/members", idKey: "member_id",
    columns: { member_id: "รหัสสมาชิก", name: "ชื่อสมาชิก", gender: "เพศ", phone: "โทรศัพท์", email: "อีเมล", join_date: "วันที่สมัคร", package_type: "แพ็กเกจ" },
    search: [{ key: "q", label: "ชื่อ / เบอร์โทร / อีเมล", type: "text" }],
    form: [
      { key: "name", label: "ชื่อสมาชิก", type: "text", required: true },
      { key: "gender", label: "เพศ", type: "select", options: ["Male", "Female", "Other"] },
      { key: "phone", label: "โทรศัพท์", type: "text" },
      { key: "email", label: "อีเมล", type: "email" },
      { key: "join_date", label: "วันที่สมัคร", type: "date", required: true },
      { key: "package_type", label: "แพ็กเกจ", type: "text" }
    ]
  },
  classes: {
    label: "คลาสฟิตเนส", api: "/api/classes", idKey: "class_id",
    columns: { class_id: "รหัสคลาส", name: "ชื่อคลาส", trainer_name: "เทรนเนอร์", room: "ห้อง", capacity: "จำนวนรับ", schedule_time: "วันและเวลา" },
    search: [{ key: "q", label: "ชื่อคลาส / ห้อง / เทรนเนอร์", type: "text" }],
    form: [
      { key: "trainer_id", label: "รหัสเทรนเนอร์", type: "number", required: true },
      { key: "name", label: "ชื่อคลาส", type: "text", required: true },
      { key: "room", label: "ห้อง", type: "text" },
      { key: "capacity", label: "จำนวนรับ", type: "number", required: true },
      { key: "schedule_time", label: "วันและเวลา", type: "datetime-local", required: true }
    ]
  },
  bookings: {
    label: "การจอง", api: "/api/bookings", idKey: "booking_id",
    columns: { booking_id: "รหัสการจอง", member_name: "สมาชิก", class_name: "คลาส", book_date: "วันที่จอง", status: "สถานะ" },
    search: [{ key: "q", label: "ชื่อสมาชิก / คลาส / สถานะ", type: "text" }],
    form: [
      { key: "member_id", label: "รหัสสมาชิก", type: "number", required: true },
      { key: "class_id", label: "รหัสคลาส", type: "number", required: true },
      { key: "book_date", label: "วันและเวลาที่จอง", type: "datetime-local", required: true },
      { key: "status", label: "สถานะ", type: "select", options: ["CONFIRMED", "CANCELLED"], required: true }
    ]
  },
  trainers: {
    label: "เทรนเนอร์", api: "/api/trainers", idKey: "trainer_id",
    columns: { trainer_id: "รหัสเทรนเนอร์", name: "ชื่อเทรนเนอร์", specialty: "ความเชี่ยวชาญ", phone: "โทรศัพท์", mentor_trainer_id: "รหัสพี่เลี้ยง" },
    search: [{ key: "q", label: "ชื่อ / ความเชี่ยวชาญ / โทรศัพท์", type: "text" }],
    form: [
      { key: "name", label: "ชื่อเทรนเนอร์", type: "text", required: true },
      { key: "specialty", label: "ความเชี่ยวชาญ", type: "text" },
      { key: "phone", label: "โทรศัพท์", type: "text" },
      { key: "mentor_trainer_id", label: "รหัสเทรนเนอร์พี่เลี้ยง", type: "number" }
    ]
  },
  equipment: {
    label: "อุปกรณ์", api: "/api/equipment", idKey: "equip_id",
    columns: { equip_id: "รหัสอุปกรณ์", name: "ชื่ออุปกรณ์", zone: "โซน", status: "สถานะ", total_quantity: "จำนวน" },
    search: [{ key: "q", label: "ชื่ออุปกรณ์ / โซน / สถานะ", type: "text" }],
    form: [
      { key: "name", label: "ชื่ออุปกรณ์", type: "text", required: true },
      { key: "zone", label: "โซน", type: "text" },
      { key: "status", label: "สถานะ", type: "text", required: true },
      { key: "total_quantity", label: "จำนวน", type: "number", required: true }
    ]
  }
};

let current = "members";
let editingId = null;
const $ = (selector) => document.querySelector(selector);

function setStatus(message, kind = "") {
  const element = $("#status");
  element.className = `status ${kind}`;
  element.textContent = message;
}

async function api(url, options = {}) {
  const response = await fetch(url, options);
  const result = await response.json();
  if (!response.ok || !result.ok) throw new Error(result.error || "ทำรายการไม่สำเร็จ");
  return result.data;
}

function createField(field, prefix, value = "") {
  const id = `${prefix}${field.key}`;
  let input;
  if (field.type === "select") {
    input = document.createElement("select");
    for (const option of field.options || []) {
      const item = document.createElement("option");
      item.value = option;
      item.textContent = option || "เลือก";
      input.append(item);
    }
    input.value = value ?? "";
  } else {
    input = document.createElement("input");
    input.type = field.type || "text";
    input.value = value ?? "";
    if (field.required) input.required = true;
    if (input.type === "datetime-local" && input.value) {
      input.value = String(input.value).replace(" ", "T").slice(0, 16);
    }
  }
  input.id = id;
  const wrapper = document.createElement("div");
  wrapper.className = "field";
  const label = document.createElement("label");
  label.htmlFor = id;
  label.textContent = field.label;
  wrapper.append(label, input);
  return wrapper;
}

function buildSearch() {
  const entity = ENTITIES[current];
  $("#searchTitle").textContent = entity.label;
  $("#searchFields").replaceChildren(...entity.search.map((field) => createField(field, "s_")));
}

function renderRows(rows) {
  const entity = ENTITIES[current];
  const head = $("#tableHead");
  const body = $("#tableBody");
  head.replaceChildren();
  body.replaceChildren();
  if (!rows.length) {
    setStatus("ไม่พบข้อมูล");
    return;
  }
  setStatus(`พบ ${rows.length} รายการ`);
  const columns = Object.entries(entity.columns);
  for (const [, label] of columns) {
    const th = document.createElement("th");
    th.textContent = label;
    head.append(th);
  }
  const actionHeader = document.createElement("th");
  actionHeader.textContent = "จัดการ";
  head.append(actionHeader);

  for (const row of rows) {
    const tr = document.createElement("tr");
    for (const [key] of columns) {
      const td = document.createElement("td");
      td.textContent = row[key] ?? "—";
      tr.append(td);
    }
    const actionCell = document.createElement("td");
    const editButton = document.createElement("button");
    editButton.className = "btn sm";
    editButton.textContent = "แก้ไข";
    editButton.onclick = () => editRow(row[entity.idKey]);
    const deleteButton = document.createElement("button");
    deleteButton.className = "btn sm del";
    deleteButton.textContent = "ลบ";
    deleteButton.onclick = () => deleteRow(row[entity.idKey]);
    actionCell.append(editButton, " ", deleteButton);
    tr.append(actionCell);
    body.append(tr);
  }
}

async function doSearch() {
  try {
    const params = new URLSearchParams();
    for (const field of ENTITIES[current].search) {
      const value = $(`#s_${field.key}`).value;
      if (value) params.set(field.key, value);
    }
    setStatus("กำลังค้นหา...");
    renderRows(await api(`${ENTITIES[current].api}?${params}`));
  } catch (error) {
    setStatus(error.message, "err");
  }
}

function openForm(title, data = {}) {
  $("#modalTitle").textContent = title;
  $("#formFields").replaceChildren(...ENTITIES[current].form.map((field) => createField(field, "f_", data[field.key])));
  $("#modal").classList.remove("hidden");
}

function collectForm() {
  const data = {};
  for (const field of ENTITIES[current].form) data[field.key] = $(`#f_${field.key}`).value;
  return data;
}

async function editRow(id) {
  try {
    editingId = id;
    openForm("แก้ไขข้อมูล", await api(`${ENTITIES[current].api}/${id}`));
  } catch (error) {
    alert(error.message);
  }
}

async function deleteRow(id) {
  if (!confirm("ยืนยันลบรายการนี้? การลบสมาชิกหรือเทรนเนอร์อาจกระทบข้อมูลที่เชื่อมโยง")) return;
  try {
    await api(`${ENTITIES[current].api}/${id}`, { method: "DELETE" });
    await doSearch();
  } catch (error) {
    alert(error.message);
  }
}

async function save() {
  const entity = ENTITIES[current];
  const url = editingId ? `${entity.api}/${editingId}` : entity.api;
  try {
    await api(url, {
      method: editingId ? "PUT" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(collectForm())
    });
    $("#modal").classList.add("hidden");
    await doSearch();
  } catch (error) {
    alert(error.message);
  }
}

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((item) => item.classList.remove("active"));
    tab.classList.add("active");
    current = tab.dataset.entity;
    editingId = null;
    buildSearch();
    doSearch();
  });
});

$("#btnSearch").onclick = doSearch;
$("#btnClear").onclick = () => { buildSearch(); doSearch(); };
$("#btnAdd").onclick = () => { editingId = null; openForm(`เพิ่ม${ENTITIES[current].label}`); };
$("#btnSave").onclick = save;
$("#btnCancel").onclick = () => $("#modal").classList.add("hidden");
buildSearch();
doSearch();

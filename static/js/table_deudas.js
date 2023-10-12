let dataTable;
let dataTableIsInitialized=false;

var editarButtons = document.querySelectorAll('.editar-button');
editarButtons.forEach(function(button) {
    button.addEventListener('click', function() {
        var id = this.getAttribute('data-id');
        // Hacer algo con el 'id', como redirigir a la página de edición
        window.location.href = '/editar_deudas/' + id;
    });
});

const dataTableOptions={
    columnDefs:[
        { className: "cole", targets: [0, 1, 2, 3, 4] },
        { orderable: false, targets: [5] },
    ],
    destroy: true,
    language: {
        lengthMenu: "Mostrar _MENU_ registros por página",
        zeroRecords: "Ninguna Deuda encontrado",
        info: "Mostrando de _START_ a _END_ de un total de _TOTAL_ registros",
        infoEmpty: "Ninguna Deuda encontrado",
        infoFiltered: "(filtrados desde _MAX_ registros totales)",
        search: "Buscar:",
        loadingRecords: "Cargando...",
        paginate: {
            first: "Primero",
            last: "Último",
            next: "Siguiente",
            previous: "Anterior"
        }
    }
};

const initDataTable = async()=>{
if(dataTableIsInitialized){
    dataTable.destroy();
}

await listDeuda();

dataTable=$('#datatable_deudas').DataTable(dataTableOptions);

dataTableIsInitialized = true;
}

const listDeuda = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/list_deuda/');
        const contentType = response.headers.get("content-type");

        if (contentType && contentType.includes("application/json")) {
            const data = await response.json();

            let content = ``;
            data.deudas.forEach(deuda => {
                content += `
                    <tr>
                        <td>${deuda.descripcion_deuda}</td>
                        <td>${deuda.dia_pago}</td>
                        <td>${deuda.valor_total_deuda}</td>
                        <td>${deuda.tipo_de_interes}</td>
                        <td>${deuda.valor_interes_mensual}</td>
                        <td>
                            <a href="${deuda.url_edicion}" type="button" class="btn btn-primary">Actualizar</a>
                            <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#staticBackdrop">Borrar</button>
                        </td>
                    </tr>
                `;
            });
            tablebody_deudas.innerHTML = content;
        } else {
            console.error("La respuesta no es JSON.");
        }
    } catch (ex) {
        console.error(ex);
    }
};


window.addEventListener('load',async()=>{
    await initDataTable();

});
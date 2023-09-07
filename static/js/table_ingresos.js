let dataTable;
let dataTableIsInitialized=false;

var editarButtons = document.querySelectorAll('.editar-button');
editarButtons.forEach(function(button) {
    button.addEventListener('click', function() {
        var id = this.getAttribute('data-id');
        // Hacer algo con el 'id', como redirigir a la página de edición
        window.location.href = '/editar_ingreso/' + id;
    });
});

const dataTableOptions={
    columnDefs:[
        { className: "cole", targets: [0, 1, 2, 3] },
        { orderable: false, targets: [3] },
    ],
    destroy: true,
    language: {
        lengthMenu: "Mostrar _MENU_ registros por página",
        zeroRecords: "Ningún Ingreso encontrado",
        info: "Mostrando de _START_ a _END_ de un total de _TOTAL_ registros",
        infoEmpty: "Ningún Ingreso encontrado",
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

await listIngresos();

dataTable=$('#datatable_ingresos').DataTable(dataTableOptions);

dataTableIsInitialized = true;
}

const listIngresos = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/list_ingreso/');
        const contentType = response.headers.get("content-type");

        if (contentType && contentType.includes("application/json")) {
            const data = await response.json();

            let content = ``;
            data.transacciones.forEach(transaccion => {
                content += `
                    <tr>
                        <td>${transaccion.fecha}</td>
                        <td>${transaccion.monto}</td>
                        <td>${transaccion.fk_fuente__nombre_fuente}</td>
                        <td>
                            <a href="${transaccion.url_edicion}" type="button" class="btn btn-primary">Actualizar</a>
                            <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#staticBackdrop">Borrar</button>
                        </td>
                    </tr>
                `;
            });
            tablebody_ingresos.innerHTML = content;
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
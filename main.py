from fastapi.responses import RedirectResponse
import uvicorn

from application.main_app import application as app


@app.get("/", name='Переадресация на страницу документации', response_class=RedirectResponse)
async def read_items():
    """Переадресация на страницу документации"""
    return RedirectResponse('/docs')




# Запуск программы
if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True)
import './Receipt.css';

function Receipt() {
    return (
        <>
            <header className='header'>매장</header>
            <div>
                <p className='oct'>결제가 완료 되었습니다.<br/></p>
                <p className='make'>영수증을</p>
                <p className='make'>출력하시겠습니까?</p>
            </div>
            <div className='coke'>
                <button className='react'>예</button>
                <button className='react'>아니오</button>
            </div>
            <div className='bread'>
                <button className='react'>주문 번호 x번</button>
            </div>
        </>
    );
}

export default Receipt;
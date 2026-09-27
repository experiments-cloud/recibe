(define (problem blocksworld-problema)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (clear a)
    (handempty)
    (on d a)
    (on b d)
    (on f b)
    (on e f)
    (on c e)
    (ontable c)
  )
  (:goal (and
    (on a e)
    (on b a)
    (on c b)
    (on d c)
    (on e d)
    (on f e)
  ))
)
